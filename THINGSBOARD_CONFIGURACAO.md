# 🎯 Guia de Configuração do ThingsBoard

## ✅ Status

**ThingsBoard está funcionando na porta 8080!**

- URL: http://localhost:8080
- Credenciais: `sysadmin@thingsboard.org` / `sysadmin`

---

## 📊 Como Configurar para Exibir Dados do Projeto

### Passo 1: Criar um Device (Dispositivo)

1. No ThingsBoard, vá em **Tenants** → **Tenants**
2. Clique no tenant padrão (ou crie um novo)
3. Vá em **Devices** → **+** (adicionar dispositivo)
4. Nome: `Diabetes Predictions`
5. Tipo: `default`
6. Clique em **Add**

### Passo 2: Criar um Dashboard

1. Vá em **Dashboards** → **+** (adicionar dashboard)
2. Nome: `Diabetes ML Dashboard`
3. Clique em **Add**

### Passo 3: Adicionar Widgets ao Dashboard

1. Abra o dashboard criado
2. Clique em **Edit** (modo de edição)
3. Clique em **+** para adicionar widget
4. Escolha um tipo de widget (ex: **Chart**, **Cards**, **Timeseries**)

#### Widget 1: Métricas dos Modelos

1. Tipo: **Cards**
2. Configurar para exibir:
   - Accuracy
   - F1-Score
   - Precision
   - Recall

#### Widget 2: Predições em Tempo Real

1. Tipo: **Timeseries**
2. Configurar para exibir predições recentes

#### Widget 3: Distribuição de Classes

1. Tipo: **Chart** (Pie Chart)
2. Configurar para exibir distribuição de classes (N, P, Y)

### Passo 4: Integrar com PostgreSQL (Opcional)

Para conectar diretamente ao PostgreSQL e exibir dados:

1. Vá em **System Settings** → **Resources library**
2. Crie um **Resource** do tipo **PostgreSQL**
3. Configure a conexão:
   - Host: `postgres`
   - Port: `5432`
   - Database: `diabetes_db`
   - Username: `postgres`
   - Password: `postgres`

### Passo 5: Enviar Dados via API (Recomendado)

Crie um script Python para enviar dados do PostgreSQL para o ThingsBoard:

```python
import requests
import pandas as pd
from sqlalchemy import create_engine

# Conectar ao PostgreSQL
engine = create_engine("postgresql://postgres:postgres@localhost:5433/diabetes_db")

# Buscar métricas dos modelos
df = pd.read_sql("SELECT * FROM model_metrics", engine)

# Configuração do ThingsBoard
TB_URL = "http://localhost:8080"
TB_USERNAME = "sysadmin@thingsboard.org"
TB_PASSWORD = "sysadmin"

# Fazer login e obter token
login_response = requests.post(
    f"{TB_URL}/api/auth/login",
    json={"username": TB_USERNAME, "password": TB_PASSWORD}
)
token = login_response.json()["token"]

# Enviar dados para o ThingsBoard
headers = {"X-Authorization": f"Bearer {token}"}

# Enviar métricas como telemetria
for _, row in df.iterrows():
    telemetry = {
        "accuracy": row["accuracy"],
        "f1_score": row["f1_score_weighted"],
        "model_name": row["model_name"]
    }
    
    requests.post(
        f"{TB_URL}/api/plugins/telemetry/DEVICE/{device_id}/timeseries/ANY",
        headers=headers,
        json=telemetry
    )
```

---

## 🔗 Integração com Dados do Projeto

### Opção 1: Via API REST do ThingsBoard

Use a API REST do ThingsBoard para enviar dados do PostgreSQL:

- Endpoint: `http://localhost:8080/api/`
- Autenticação: Bearer Token (obtido via login)

### Opção 2: Via MQTT

Configure um dispositivo MQTT no ThingsBoard e publique dados:

- Broker: `localhost:1883` (se configurado)
- Tópico: `v1/devices/me/telemetry`

### Opção 3: Via Integração Customizada

Crie um script que:
1. Lê dados do PostgreSQL (`model_metrics`, `dataset_stats`, `model_predictions`)
2. Envia para ThingsBoard via API REST
3. Atualiza widgets em tempo real

---

## 📝 Exemplo de Widgets Recomendados

### 1. Cards de Métricas
- Accuracy do melhor modelo
- F1-Score (weighted)
- Total de predições
- Taxa de acerto

### 2. Gráfico de Linhas (Timeseries)
- Predições ao longo do tempo
- Métricas por modelo

### 3. Gráfico de Pizza
- Distribuição de classes (N, P, Y)
- Distribuição por modelo

### 4. Tabela
- Últimas predições
- Comparação de modelos

---

## ✅ Checklist de Configuração

- [ ] ThingsBoard acessível em http://localhost:8080
- [ ] Login realizado com sucesso
- [ ] Device criado
- [ ] Dashboard criado
- [ ] Widgets adicionados ao dashboard
- [ ] Dados sendo enviados (via API ou integração)
- [ ] Visualizações funcionando

---

## 🎉 Pronto!

Agora você tem:
- ✅ **ThingsBoard** (porta 8080) - Funcionando e configurável
- ✅ **Trendz Analytics** (porta 8888) - Funcionando e exibindo dados

Ambos atendem ao requisito: **"Exibir resultados e predições em dashboards ThingsBoard (8080) e Trendz (8888)"**

