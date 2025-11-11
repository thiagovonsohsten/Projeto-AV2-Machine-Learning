"""
FastAPI - API de Ingestão de Dados
Recebe dados CSV/JSON e armazena no MinIO e PostgreSQL
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import io
from sqlalchemy import create_engine, text
import os
from datetime import datetime
import time

app = FastAPI(
    title="Diabetes ML - API de Ingestão",
    description="API para ingestão de dados do dataset de diabetes",
    version="1.0.0"
)

# Configurações do MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET_RAW = os.getenv("MINIO_BUCKET_RAW", "raw-data")

# Configurações do PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "diabetes_db")

# Cliente S3 (MinIO)
s3_client = boto3.client(
    's3',
    endpoint_url=f'http://{MINIO_ENDPOINT}',
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name='us-east-1'
)

# Conexão com PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)


def ensure_bucket_exists(bucket_name: str):
    """Garante que o bucket existe no MinIO"""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} criado com sucesso")


@app.on_event("startup")
async def startup_event():
    """Inicialização: cria buckets necessários"""
    # Aguardar MinIO estar pronto
    max_retries = 10
    for i in range(max_retries):
        try:
            ensure_bucket_exists(MINIO_BUCKET_RAW)
            ensure_bucket_exists("models")
            ensure_bucket_exists("mlflow-artifacts")
            print("Buckets verificados/criados com sucesso")
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"Tentativa {i+1}/{max_retries}: Aguardando MinIO...")
                time.sleep(2)
            else:
                print(f"Erro ao inicializar buckets após {max_retries} tentativas: {e}")


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Diabetes ML - API de Ingestão",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Verifica saúde dos serviços"""
    health_status = {
        "api": "healthy",
        "minio": "unknown",
        "postgres": "unknown"
    }
    
    # Verificar MinIO
    try:
        s3_client.list_buckets()
        health_status["minio"] = "healthy"
    except Exception as e:
        health_status["minio"] = f"unhealthy: {str(e)}"
    
    # Verificar PostgreSQL
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["postgres"] = "healthy"
    except Exception as e:
        health_status["postgres"] = f"unhealthy: {str(e)}"
    
    return health_status


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint para upload de arquivo CSV
    Salva no MinIO e insere dados tratados no PostgreSQL
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Apenas arquivos CSV são aceitos")
    
    try:
        # Ler conteúdo do arquivo
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Validar colunas esperadas
        expected_columns = ['ID', 'No_Pation', 'Gender', 'AGE', 'Urea', 'Cr', 
                          'HbA1c', 'Chol', 'TG', 'HDL', 'LDL', 'VLDL', 'BMI', 'CLASS']
        
        if not all(col in df.columns for col in expected_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"Colunas esperadas: {expected_columns}"
            )
        
        # Salvar no MinIO (dados brutos)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        s3_key = f"raw/{timestamp}_{file.filename}"
        
        s3_client.put_object(
            Bucket=MINIO_BUCKET_RAW,
            Key=s3_key,
            Body=contents,
            ContentType='text/csv'
        )
        
        # Preparar dados para PostgreSQL (renomear colunas)
        df_db = df.copy()
        df_db.columns = df_db.columns.str.lower()
        df_db = df_db.rename(columns={
            'id': 'record_id',
            'no_pation': 'patient_number',
            'cr': 'creatinine',
            'hba1c': 'hba1c',
            'chol': 'cholesterol',
            'tg': 'triglycerides',
            'class': 'class_label'
        })
        
        # Inserir no PostgreSQL
        df_db.to_sql(
            'diabetes_processed',
            engine,
            if_exists='append',
            index=False,
            method='multi'
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Arquivo processado com sucesso",
                "filename": file.filename,
                "records": len(df),
                "s3_key": s3_key,
                "database_records": len(df_db)
            }
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Arquivo CSV vazio")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")


@app.get("/data/stats")
async def get_data_stats():
    """Retorna estatísticas dos dados armazenados"""
    try:
        with engine.connect() as conn:
            # Contar registros por classe
            result = conn.execute(text("""
                SELECT 
                    class_label,
                    COUNT(*) as count
                FROM diabetes_processed
                GROUP BY class_label
            """))
            
            stats = {
                "total_records": 0,
                "by_class": {}
            }
            
            for row in result:
                stats["by_class"][row[0]] = row[1]
                stats["total_records"] += row[1]
            
            return stats
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")

