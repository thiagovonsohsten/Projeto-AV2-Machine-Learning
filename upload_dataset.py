"""
Script para fazer upload do dataset via API FastAPI
Uso: python upload_dataset.py
"""

import requests
import sys
import os

API_URL = "http://localhost:8000"
DATASET_FILE = "Dataset of Diabetes .csv"

def upload_dataset():
    """Faz upload do dataset para a API"""
    
    # Verificar se o arquivo existe
    if not os.path.exists(DATASET_FILE):
        print(f"❌ Arquivo '{DATASET_FILE}' não encontrado!")
        print(f"   Certifique-se de que o arquivo está no diretório atual.")
        return False
    
    # Verificar se a API está rodando
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ API não está respondendo corretamente (status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Não foi possível conectar à API em {API_URL}")
        print(f"   Certifique-se de que os serviços estão rodando: docker-compose up -d")
        return False
    
    # Fazer upload
    print(f"📤 Fazendo upload de '{DATASET_FILE}'...")
    
    try:
        with open(DATASET_FILE, 'rb') as f:
            files = {'file': (DATASET_FILE, f, 'text/csv')}
            response = requests.post(f"{API_URL}/upload", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload realizado com sucesso!")
            print(f"   📊 Registros processados: {result['records']}")
            print(f"   💾 S3 Key: {result['s3_key']}")
            print(f"   🗄️  Registros no banco: {result['database_records']}")
            return True
        else:
            print(f"❌ Erro no upload (status: {response.status_code})")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao fazer upload: {str(e)}")
        return False

def get_stats():
    """Obtém estatísticas dos dados"""
    try:
        response = requests.get(f"{API_URL}/data/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print("\n📊 Estatísticas dos Dados:")
            print(f"   Total de registros: {stats['total_records']}")
            print("   Por classe:")
            for class_label, count in stats['by_class'].items():
                print(f"     {class_label}: {count}")
        else:
            print(f"⚠️  Não foi possível obter estatísticas (status: {response.status_code})")
    except Exception as e:
        print(f"⚠️  Erro ao obter estatísticas: {str(e)}")

if __name__ == "__main__":
    print("=" * 50)
    print("Upload de Dataset - Diabetes ML")
    print("=" * 50)
    print()
    
    if upload_dataset():
        get_stats()
        print("\n✅ Processo concluído com sucesso!")
        sys.exit(0)
    else:
        print("\n❌ Falha no processo de upload")
        sys.exit(1)

