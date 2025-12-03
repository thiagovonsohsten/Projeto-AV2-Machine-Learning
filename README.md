# Projeto AV2 - Machine Learning: Predição de Diabetes

## 📋 Sobre o Projeto

Este projeto implementa um pipeline completo de Machine Learning para classificação de diabetes, reproduzindo e melhorando o artigo científico **"Comparative Effectiveness of Classification Algorithms in Predicting Diabetes"**.

O projeto utiliza uma arquitetura baseada em contêineres Docker, integrando coleta, processamento, modelagem e visualização de dados.

## 🏗️ Arquitetura

O projeto implementa a seguinte arquitetura:

```
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌──────────┐
│ FastAPI │────▶│  MinIO  │────▶│PostgreSQL│────▶│JupyterLab│
│ (8000)  │     │ (9000)  │     │  (5432)  │     │  (8888)  │
└─────────┘     └─────────┘     └──────────┘     └──────────┘
                                                         │
                                                         ▼
                                                ┌──────────┐
                                                │  MLFlow  │
                                                │  (5000)  │
                                                └──────────┘
```

### Componentes

- **FastAPI** (Porta 8000): API REST para ingestão de dados CSV/JSON
- **MinIO** (Portas 9000/9001): Armazenamento de objetos compatível com S3
- **PostgreSQL** (Porta 5433 externa): Banco de dados relacional para dados estruturados
- **JupyterLab** (Porta 8889): Ambiente de análise e modelagem
- **MLFlow** (Porta 5000): Rastreamento de experimentos e versionamento de modelos
- **ThingsBoard** (Porta 8080): Dashboard de visualização IoT com dashboards interativos
  - Integração automática via `thingsboard_integration` (sincroniza dados a cada 5 minutos)
  - Exibe métricas, predições e estatísticas em tempo real
- **Trendz Analytics** (Porta 8888): Dashboard de visualização Streamlit - conforme especificação
- **Dashboard Streamlit** (Porta 8501): Dashboard interativo adicional

## 📁 Estrutura do Projeto

```
/
├── docker-compose.yml          # Orquestração dos contêineres
├── init_db.sql                 # Script de inicialização do banco
├── fastapi/                    # API de ingestão
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── jupyterlab/                 # Ambiente de análise
│   └── Dockerfile
├── mlflow/                     # Configuração MLFlow
├── notebooks/                  # Notebooks de análise e modelagem
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_preprocessing_and_modeling.ipynb
│   ├── 03_hyperparameter_tuning.ipynb
│   └── 04_export_to_dashboard.ipynb
├── dashboard/                  # Dashboard Streamlit
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── trendz/                     # Trendz Analytics (Dashboard Streamlit)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── thingsboard/                # Integração ThingsBoard
│   ├── integrate_to_thingsboard.py
│   ├── GUIA_DASHBOARD_THINGSBOARD.md
│   └── requirements.txt
├── reports/                    # Figuras e plots dos resultados
├── Dataset of Diabetes .csv    # Dataset original
└── README.md                   # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose v2.0+
- 8GB+ de RAM disponível
- Portas 8000, 5000, 5433, 8080, 8501, 8888, 8889, 9000, 9001 disponíveis
- ⚠️ Nota: A porta 5432 pode estar em uso por PostgreSQL local, então usamos 5433 externamente

### Passo 1: Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd Projeto-AV2-Machine-Learning
```

### Passo 2: Iniciar os Serviços

```bash
docker-compose up -d
```

Este comando irá:
- Baixar as imagens necessárias
- Criar os contêineres
- Configurar os volumes
- Inicializar os serviços

### Passo 3: Verificar Status dos Serviços

```bash
docker-compose ps
```

Todos os serviços devem estar com status "Up" e "healthy".

### Passo 4: Upload do Dataset

#### Opção 1: Script Python (Mais Fácil)

```bash
# Instalar dependências (se necessário)
pip install requests

# Executar script de upload
python upload_dataset.py
```

#### Opção 2: Via API com cURL

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@Dataset of Diabetes .csv"
```

#### Opção 3: Via Interface Web

Acesse `http://localhost:8000/docs` e use a interface Swagger para fazer upload.

### Passo 5: Acessar os Serviços

- **FastAPI**: http://localhost:8000
- **FastAPI Docs**: http://localhost:8000/docs
- **JupyterLab**: http://localhost:8889 ⭐ (mudado para liberar 8888 para Trendz)
- **MLFlow**: http://localhost:5000
- **Trendz Analytics**: http://localhost:8888 ⭐ **Dashboard Principal (conforme especificação)**
- **ThingsBoard**: http://localhost:8080 ⭐ **Dashboard Principal (conforme especificação)**
  - Credenciais: `sysadmin@thingsboard.org` / `sysadmin`
- **Dashboard Streamlit**: http://localhost:8501 (dashboard adicional)
- **MinIO Console**: http://localhost:9001 (usuário: minioadmin, senha: minioadmin)

> **Nota**: Ambos os dashboards (ThingsBoard e Trendz Analytics) estão funcionando conforme especificação. O Trendz Analytics já está exibindo dados automaticamente.

### Passo 6: Executar Análise

1. Acesse o JupyterLab em http://localhost:8889
2. Execute os notebooks na seguinte ordem:
   - `01_exploratory_data_analysis.ipynb` - Análise exploratória
   - `02_preprocessing_and_modeling.ipynb` - Treinamento de modelos
   - `03_hyperparameter_tuning.ipynb` - Ajuste de hiperparâmetros (opcional)
   - `04_export_to_dashboard.ipynb` - Exportar dados para dashboard

### Passo 7: Visualizar nos Dashboards

#### Opção 1: Trendz Analytics (Automático)
1. Execute o notebook `04_export_to_dashboard.ipynb` para exportar dados
2. Acesse o Trendz Analytics em http://localhost:8888
3. Visualize automaticamente:
   - Estatísticas do dataset
   - Métricas dos modelos
   - Predições e distribuições

#### Opção 2: ThingsBoard (Requer Configuração)
1. Execute o notebook `04_export_to_dashboard.ipynb` para exportar dados
2. Aguarde a sincronização automática (ou execute manualmente):
   ```bash
   docker-compose restart thingsboard_integration
   ```
3. Acesse o ThingsBoard em http://localhost:8080
4. Siga o guia em `thingsboard/GUIA_DASHBOARD_THINGSBOARD.md` para:
   - Verificar dispositivos criados
   - Criar dashboard
   - Adicionar widgets interativos
   - Configurar visualizações

#### Opção 3: Dashboard Streamlit (Alternativo)
1. Execute o notebook `04_export_to_dashboard.ipynb` para exportar dados
2. Acesse o Dashboard Streamlit em http://localhost:8501
3. Navegue pelas páginas:
   - **Visão Geral**: Estatísticas do dataset
   - **Análise de Dados**: Visualizações interativas
   - **Modelos ML**: Comparação de modelos
   - **Métricas e Resultados**: Análise detalhada

## 📊 Dataset

O dataset contém:
- **1001 registros** de pacientes
- **13 features**: ID, No_Pation, Gender, AGE, Urea, Cr, HbA1c, Chol, TG, HDL, LDL, VLDL, BMI
- **Classe alvo**: CLASS (N=Non-diabetic, P=Prediabetic, Y=Diabetic)

## 🔬 Modelos Implementados

O projeto implementa e compara os seguintes algoritmos de classificação:

1. **Random Forest** (com ajuste de hiperparâmetros)
2. **Gradient Boosting** (com ajuste de hiperparâmetros)
3. **Support Vector Machine (SVM)**
4. **Logistic Regression**
5. **K-Nearest Neighbors (KNN)**

### Melhorias Implementadas:

- ✅ **Ajuste de Hiperparâmetros**: GridSearchCV para otimização
- ✅ **Validação Cruzada**: 5-fold cross-validation
- ✅ **Balanceamento**: SMOTE para lidar com classes desbalanceadas
- ✅ **Normalização**: StandardScaler para padronização
- ✅ **Registro Completo**: Todos os experimentos no MLFlow
- ✅ **Dashboard Interativo**: Visualização de resultados em tempo real

Todos os experimentos são registrados no MLFlow para comparação e versionamento.

## 📈 Métricas de Avaliação

- **Accuracy** (Acurácia)
- **F1-Score** (ponderado e macro)
- **Precision e Recall** por classe
- **Classification Report** completo
- **Confusion Matrix** (numérica e normalizada)
- **Validação Cruzada** (5-fold)
- **Feature Importance** (para modelos baseados em árvore)

## 🛠️ Comandos Úteis

### Parar os serviços
```bash
docker-compose down
```

### Parar e remover volumes (limpar dados)
```bash
docker-compose down -v
```

### Ver logs de um serviço específico
```bash
docker-compose logs -f fastapi
docker-compose logs -f jupyterlab
docker-compose logs -f mlflow
```

### Reiniciar um serviço específico
```bash
docker-compose restart fastapi
```

### Acessar shell de um contêiner
```bash
docker-compose exec jupyterlab bash
docker-compose exec postgres psql -U postgres -d diabetes_db
```

## 📝 Melhorias Implementadas

Além de reproduzir o artigo original, foram implementadas as seguintes melhorias:

1. **Balanceamento de dados**: SMOTE para lidar com desbalanceamento de classes
2. **Normalização**: StandardScaler para padronizar features
3. **Ajuste de Hiperparâmetros**: GridSearchCV com validação cruzada
4. **Validação Cruzada**: 5-fold CV para avaliação robusta
5. **MLFlow**: Rastreamento completo de experimentos e versionamento
6. **Dashboard Interativo**: Streamlit para visualização de resultados
7. **ThingsBoard**: Dashboard IoT para monitoramento (opcional)
8. **Pipeline Automatizado**: Integração completa entre componentes
9. **Exportação Automática**: Métricas e resultados salvos no banco
10. **API REST**: Endpoints para acesso aos dados e métricas

## 🐛 Troubleshooting

### Erro: Porta já em uso
```bash
# Verificar qual processo está usando a porta
netstat -ano | findstr :8000

# Parar o processo ou alterar a porta no docker-compose.yml
```

### Erro: Contêiner não inicia
```bash
# Verificar logs
docker-compose logs <nome-do-servico>

# Reconstruir imagens
docker-compose build --no-cache
docker-compose up -d
```

### Erro: MinIO não conecta
```bash
# Verificar se o MinIO está saudável
docker-compose ps minio

# Verificar logs
docker-compose logs minio
```

## 📚 Referências

- Artigo original: "Comparative Effectiveness of Classification Algorithms in Predicting Diabetes"
- Dataset: Dataset of Diabetes.csv
- Documentação FastAPI: https://fastapi.tiangolo.com/
- Documentação MLFlow: https://mlflow.org/
- Documentação MinIO: https://min.io/docs/

## 👥 Equipe

- Thiago von Sohsten (@thiagovonsohsten)
- Enzo Nunes (@ebn0511)
- Felipe Sérgio (@felipesergiob)
- Thiago Belo (@thiagombelo)
- Sérgio Mariano (@sergiogmariano)


## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🎓 Instituição

**CESAR School**  
Disciplina: Aprendizado de Máquina - 2025.2  
Período: 2ª Unidade

---

**Nota**: Este projeto foi desenvolvido para fins acadêmicos como parte da avaliação da disciplina de Aprendizado de Máquina.
