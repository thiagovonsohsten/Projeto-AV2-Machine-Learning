#!/usr/bin/env python3
"""
Script de Integração ThingsBoard - Projeto Diabetes ML

Este script:
1. Conecta ao ThingsBoard via API REST
2. Cria dispositivos para cada modelo de ML
3. Envia métricas e predições do PostgreSQL para ThingsBoard
4. Cria dashboard com widgets interativos
"""

import requests
import pandas as pd
from sqlalchemy import create_engine, text
import os
import json
import time
from typing import Dict, List, Optional

# Configurações
# Quando executado dentro do Docker, usa o nome do serviço
# Quando executado localmente, usa localhost
TB_INTERNAL_URL = os.getenv('THINGSBOARD_URL', 'http://thingsboard:9090')
TB_EXTERNAL_URL = 'http://localhost:8080'
TB_URL = TB_INTERNAL_URL if os.getenv('THINGSBOARD_URL') else TB_EXTERNAL_URL
TB_USERNAME = os.getenv('THINGSBOARD_USERNAME', 'admin@diabetes-ml.com')
TB_PASSWORD = os.getenv('THINGSBOARD_PASSWORD', 'admin123')

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'diabetes_db')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


class ThingsBoardIntegration:
    """Classe para integração com ThingsBoard"""
    
    def __init__(self):
        self.url = TB_URL
        self.token = None
        self.headers = None
        self.engine = create_engine(DATABASE_URL)
        self.devices = {}  # Cache de devices criados
        self.dashboard_id = None
        
    def login(self) -> bool:
        """Faz login no ThingsBoard e obtém token"""
        max_retries = 5
        retry_delay = 10  # segundos
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.url}/api/auth/login",
                    json={"username": TB_USERNAME, "password": TB_PASSWORD},
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.token = response.json()["token"]
                    self.headers = {
                        "X-Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    }
                    print("✅ Login no ThingsBoard realizado com sucesso!")
                    
                    # Verificar informações do usuário logado
                    try:
                        user_info = requests.get(
                            f"{self.url}/api/auth/user",
                            headers=self.headers
                        )
                        if user_info.status_code == 200:
                            user_data = user_info.json()
                            print(f"   Usuário: {user_data.get('email', 'N/A')}")
                            print(f"   Autoridade: {user_data.get('authority', 'N/A')}")
                    except:
                        pass
                    
                    return True
                else:
                    print(f"⚠️ Tentativa {attempt + 1}/{max_retries}: Erro no login: {response.status_code}")
                    if attempt < max_retries - 1:
                        print(f"   Aguardando {retry_delay} segundos antes de tentar novamente...")
                        time.sleep(retry_delay)
            except requests.exceptions.ConnectionError as e:
                print(f"⚠️ Tentativa {attempt + 1}/{max_retries}: ThingsBoard não está acessível ainda")
                if attempt < max_retries - 1:
                    print(f"   Aguardando {retry_delay} segundos antes de tentar novamente...")
                    time.sleep(retry_delay)
            except Exception as e:
                print(f"❌ Erro ao conectar ao ThingsBoard: {e}")
                if attempt < max_retries - 1:
                    print(f"   Aguardando {retry_delay} segundos antes de tentar novamente...")
                    time.sleep(retry_delay)
        
        print("❌ Falha no login após todas as tentativas")
        return False
    
    def get_or_create_device(self, device_name: str, device_type: str = "Diabetes Model") -> Optional[str]:
        """Obtém ou cria um device no ThingsBoard"""
        if device_name in self.devices:
            return self.devices[device_name]
        
        try:
            # Buscar device existente (API de tenant admin)
            response = requests.get(
                f"{self.url}/api/tenant/devices",
                headers=self.headers,
                params={"textSearch": device_name, "pageSize": 100}
            )
            
            if response.status_code == 200:
                devices = response.json().get("data", [])
                # Procurar device com nome exato
                for device in devices:
                    if device.get("name") == device_name:
                        device_id = device["id"]["id"]
                        self.devices[device_name] = device_id
                        print(f"✅ Device '{device_name}' encontrado: {device_id}")
                        return device_id
            elif response.status_code == 403:
                print(f"⚠️ Sem permissão para buscar devices. Tentando criar diretamente...")
            
            # Tentar criar device (pode falhar se não tiver permissão)
            device_data = {
                "name": device_name,
                "type": device_type,
                "label": device_name
            }
            
            response = requests.post(
                f"{self.url}/api/device",
                headers=self.headers,
                json=device_data
            )
            
            if response.status_code == 200:
                device_id = response.json()["id"]["id"]
                self.devices[device_name] = device_id
                print(f"✅ Device '{device_name}' criado: {device_id}")
                return device_id
            else:
                # Device não existe e não pode ser criado via API
                print(f"⚠️ Device '{device_name}' não encontrado e não pode ser criado via API (403)")
                print(f"   💡 Crie o device manualmente no ThingsBoard:")
                print(f"      1. Faça login como tenant admin")
                print(f"      2. Vá em Devices → +")
                print(f"      3. Nome: {device_name}")
                print(f"      4. Type: {device_type}")
                print(f"   Veja o guia: thingsboard/CRIAR_DEVICES_MANUALMENTE.md")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao obter/criar device '{device_name}': {e}")
            return None
    
    def send_telemetry(self, device_id: str, telemetry: Dict) -> bool:
        """Envia telemetria para um device"""
        try:
            response = requests.post(
                f"{self.url}/api/plugins/telemetry/DEVICE/{device_id}/timeseries/ANY",
                headers=self.headers,
                json=telemetry
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"⚠️ Erro ao enviar telemetria: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar telemetria: {e}")
            return False
    
    def create_dashboard(self, dashboard_name: str = "Diabetes ML Dashboard") -> Optional[str]:
        """Cria um dashboard no ThingsBoard"""
        try:
            # Verificar se dashboard já existe
            response = requests.get(
                f"{self.url}/api/dashboard",
                headers=self.headers,
                params={"textSearch": dashboard_name}
            )
            
            if response.status_code == 200:
                dashboards = response.json().get("data", [])
                if dashboards:
                    dashboard_id = dashboards[0]["id"]["id"]
                    self.dashboard_id = dashboard_id
                    print(f"✅ Dashboard '{dashboard_name}' encontrado: {dashboard_id}")
                    return dashboard_id
            
            # Criar novo dashboard
            dashboard_data = {
                "title": dashboard_name,
                "configuration": {
                    "widgets": {},
                    "states": {},
                    "entityAliases": {},
                    "filters": {},
                    "timewindow": {
                        "displayValue": "",
                        "selectedTab": 0,
                        "realtime": {
                            "timewindowMs": 60000
                        },
                        "history": {
                            "timewindowMs": 3600000,
                            "interval": 1000,
                            "aggregation": "AVG"
                        }
                    }
                }
            }
            
            response = requests.post(
                f"{self.url}/api/dashboard",
                headers=self.headers,
                json=dashboard_data
            )
            
            if response.status_code == 200:
                dashboard_id = response.json()["id"]["id"]
                self.dashboard_id = dashboard_id
                print(f"✅ Dashboard '{dashboard_name}' criado: {dashboard_id}")
                return dashboard_id
            else:
                print(f"❌ Erro ao criar dashboard: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao criar dashboard: {e}")
            return None
    
    def sync_model_metrics(self):
        """Sincroniza métricas dos modelos do PostgreSQL para ThingsBoard"""
        print("\n" + "=" * 60)
        print("SINCRONIZANDO MÉTRICAS DOS MODELOS")
        print("=" * 60)
        
        try:
            # Buscar métricas do banco
            query = """
                SELECT 
                    model_name,
                    accuracy,
                    f1_score_weighted,
                    f1_score_macro,
                    precision_n,
                    precision_p,
                    precision_y,
                    recall_n,
                    recall_p,
                    recall_y,
                    created_at
                FROM model_metrics
                ORDER BY created_at DESC
            """
            
            df = pd.read_sql(query, self.engine)
            
            if df.empty:
                print("⚠️ Nenhuma métrica encontrada no banco de dados")
                return
            
            # Agrupar por modelo (pegar a última versão de cada modelo)
            df_latest = df.groupby('model_name').first().reset_index()
            
            print(f"\n📊 Encontradas métricas para {len(df_latest)} modelos:")
            
            for _, row in df_latest.iterrows():
                model_name = row['model_name']
                device_id = self.get_or_create_device(f"Model_{model_name.replace(' ', '_')}")
                
                if device_id:
                    telemetry = {
                        "accuracy": float(row['accuracy']),
                        "f1_score_weighted": float(row['f1_score_weighted']),
                        "f1_score_macro": float(row['f1_score_macro']),
                        "precision_n": float(row['precision_n']),
                        "precision_p": float(row['precision_p']),
                        "precision_y": float(row['precision_y']),
                        "recall_n": float(row['recall_n']),
                        "recall_p": float(row['recall_p']),
                        "recall_y": float(row['recall_y']),
                        "model_name": model_name
                    }
                    
                    if self.send_telemetry(device_id, telemetry):
                        print(f"  ✅ Métricas de '{model_name}' enviadas")
                    else:
                        print(f"  ❌ Erro ao enviar métricas de '{model_name}'")
            
            print("\n✅ Sincronização de métricas concluída!")
            
        except Exception as e:
            print(f"❌ Erro ao sincronizar métricas: {e}")
    
    def sync_predictions(self, limit: int = 100):
        """Sincroniza predições do PostgreSQL para ThingsBoard"""
        print("\n" + "=" * 60)
        print("SINCRONIZANDO PREDIÇÕES")
        print("=" * 60)
        
        try:
            # Buscar predições recentes
            query = """
                SELECT 
                    model_name,
                    predicted_class,
                    confidence_score,
                    created_at
                FROM model_predictions
                ORDER BY created_at DESC
                LIMIT :limit
            """
            
            df = pd.read_sql(text(query), self.engine, params={'limit': limit})
            
            if df.empty:
                print("⚠️ Nenhuma predição encontrada no banco de dados")
                return
            
            print(f"\n📉 Encontradas {len(df)} predições recentes")
            
            # Agrupar por modelo e classe
            for model_name in df['model_name'].unique():
                model_df = df[df['model_name'] == model_name]
                device_id = self.get_or_create_device(f"Model_{model_name.replace(' ', '_')}")
                
                if device_id:
                    # Contar predições por classe
                    class_counts = model_df['predicted_class'].value_counts().to_dict()
                    avg_confidence = model_df['confidence_score'].mean()
                    
                    telemetry = {
                        "predictions_count": len(model_df),
                        "avg_confidence": float(avg_confidence),
                        "class_n_count": int(class_counts.get('N', 0)),
                        "class_p_count": int(class_counts.get('P', 0)),
                        "class_y_count": int(class_counts.get('Y', 0)),
                        "last_prediction_time": int(time.time() * 1000)  # timestamp em ms
                    }
                    
                    if self.send_telemetry(device_id, telemetry):
                        print(f"  ✅ Predições de '{model_name}' enviadas")
                    else:
                        print(f"  ❌ Erro ao enviar predições de '{model_name}'")
            
            print("\n✅ Sincronização de predições concluída!")
            
        except Exception as e:
            print(f"❌ Erro ao sincronizar predições: {e}")
    
    def sync_dataset_stats(self):
        """Sincroniza estatísticas do dataset para ThingsBoard"""
        print("\n" + "=" * 60)
        print("SINCRONIZANDO ESTATÍSTICAS DO DATASET")
        print("=" * 60)
        
        try:
            query = "SELECT * FROM dataset_stats ORDER BY updated_at DESC LIMIT 1"
            df = pd.read_sql(query, self.engine)
            
            if df.empty:
                print("⚠️ Nenhuma estatística encontrada no banco de dados")
                return
            
            row = df.iloc[0]
            device_id = self.get_or_create_device("Dataset_Stats", "Dataset Statistics")
            
            if device_id:
                telemetry = {
                    "total_records": int(row['total_records']),
                    "class_n_count": int(row['class_n_count']),
                    "class_p_count": int(row['class_p_count']),
                    "class_y_count": int(row['class_y_count']),
                    "avg_age": float(row['avg_age']),
                    "avg_hba1c": float(row['avg_hba1c']),
                    "avg_bmi": float(row['avg_bmi'])
                }
                
                if self.send_telemetry(device_id, telemetry):
                    print("✅ Estatísticas do dataset enviadas")
                else:
                    print("❌ Erro ao enviar estatísticas")
            
        except Exception as e:
            print(f"❌ Erro ao sincronizar estatísticas: {e}")
    
    def run_full_sync(self):
        """Executa sincronização completa"""
        print("\n" + "=" * 60)
        print("INTEGRAÇÃO THINGSBOARD - SINCRONIZAÇÃO COMPLETA")
        print("=" * 60)
        
        if not self.login():
            print("❌ Falha no login. Abortando sincronização.")
            return False
        
        # Criar dashboard
        self.create_dashboard()
        
        # Sincronizar dados
        self.sync_dataset_stats()
        self.sync_model_metrics()
        self.sync_predictions()
        
        print("\n" + "=" * 60)
        print("✅ SINCRONIZAÇÃO COMPLETA FINALIZADA!")
        print("=" * 60)
        print(f"\n📊 Acesse o ThingsBoard em: http://localhost:8080")
        if self.dashboard_id:
            print(f"   Dashboard: http://localhost:8080/dashboards/{self.dashboard_id}")
        print("\n💡 Dica: Configure os widgets manualmente no dashboard para visualizar os dados!")
        print("   Veja o guia em: thingsboard/GUIA_DASHBOARD_THINGSBOARD.md")
        
        return True


def main():
    """Função principal"""
    integration = ThingsBoardIntegration()
    integration.run_full_sync()


if __name__ == "__main__":
    main()

