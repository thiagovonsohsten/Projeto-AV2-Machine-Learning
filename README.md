# Projeto AV2 - Machine Learning: Predição de Diabetes

## 📋 Sobre o Projeto

Este projeto implementa um pipeline completo de Machine Learning para classificação de diabetes, reproduzindo e melhorando o artigo científico **"Comparative Effectiveness of Classification Algorithms in Predicting Diabetes"**.

O projeto utiliza uma arquitetura baseada em contêineres Docker, integrando coleta, processamento, modelagem e visualização de dados conforme especificação da disciplina.

## 🏗️ Arquitetura

O projeto implementa a arquitetura integrada conforme Figura 1:

```
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌──────────┐
│ FastAPI │────▶│  MinIO  │────▶│PostgreSQL│────▶│JupyterLab│
│ (8000)  │     │ (9000)  │     │  (5433)  │     │  (8889)  │
└─────────┘     └─────────┘     └──────────┘     └──────────┘
                                                         │
                                                         ▼
                                                ┌──────────┐
                                                │  MLFlow  │
                                                │  (5000)  │
                                                └──────────┘
                                                         │
                                                         ▼
                                                ┌──────────┐
                                                │Dashboard │
                                                │ (8501)   │
                                                └──────────┘
```

### Componentes

- **FastAPI** (Porta 8000): Interface de ingestão dos dados (CSV/JSON) e integração com S3
- **MinIO** (Portas 9000/9001): Armazenamento de dados brutos e modelos (S3-compatible)
- **PostgreSQL** (Porta 5433 externa): Estruturação de dados tratados
- **JupyterLab** (Porta 8889): Ambiente de análise, limpeza e modelagem preditiva
- **MLFlow** (Porta 5000): Registro e versionamento dos modelos de ML
- **Dashboard Streamlit** (Porta 8501): Visualização dos dados e dashboards interativos

## 📁 Estrutura do Projeto

```
/
├── docker-compose.yml          # Orquestração dos contêineres
├── init_db.sql                 # Script de inicialização do banco
├── fastapi/                    # Camada de ingestão (API)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── jupyterlab/                 # Ambiente de análise e exploração
│   └── Dockerfile
├── mlflow/                     # Configuração e armazenamento de experimentos
│   └── Dockerfile
├── notebooks/                   # Notebooks de tratamento, visualização e modelagem
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_preprocessing_and_modeling.ipynb
│   ├── 03_hyperparameter_tuning.ipynb
│   └── 04_export_to_dashboard.ipynb
├── dashboard/                  # Dashboard Streamlit
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── reports/                    # Figuras com os plots dos resultados
├── Dataset of Diabetes .csv    # Dataset original
├── README.md                   # Descrição do projeto
└── LICENSE                     # Licença
```

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose v2.0+
- 8GB+ de RAM disponível
- Portas 8000, 5000, 5433, 8501, 8889, 9000, 9001 disponíveis

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

#### Opção 1: Script Python

```bash
pip install requests
python upload_dataset.py
```

#### Opção 2: Via API com cURL

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@Dataset of Diabetes .csv"
```

#### Opção 3: Via Interface Web

Acesse `http://localhost:8000/docs` e use a interface Swagger.

### Passo 5: Acessar os Serviços

- **FastAPI**: http://localhost:8000
- **FastAPI Docs**: http://localhost:8000/docs
- **JupyterLab**: http://localhost:8889
- **MLFlow**: http://localhost:5000
- **Dashboard Streamlit**: http://localhost:8501
- **MinIO Console**: http://localhost:9001 (usuário: minioadmin, senha: minioadmin)

### Passo 6: Executar Análise

1. Acesse o JupyterLab em http://localhost:8889
2. Execute os notebooks na seguinte ordem:
   - `01_exploratory_data_analysis.ipynb` - Análise exploratória
   - `02_preprocessing_and_modeling.ipynb` - Treinamento de modelos
   - `03_hyperparameter_tuning.ipynb` - Ajuste de hiperparâmetros
   - `04_export_to_dashboard.ipynb` - Exportar dados para dashboard

### Passo 7: Visualizar no Dashboard

1. Execute o notebook `04_export_to_dashboard.ipynb` para exportar dados
2. Acesse o Dashboard Streamlit em http://localhost:8501
3. Navegue pelas páginas:
   - **Visão Geral**: Estatísticas do dataset
   - **Análise de Dados**: Visualizações interativas
   - **Modelos ML**: Comparação de modelos
   - **Métricas e Resultados**: Análise detalhada

## 📊 Dataset

O dataset contém:
- **5000+ registros** de pacientes
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

## 📝 Fluxo Geral

1. **FastAPI** recebe e armazena os dados no S3/MinIO
2. Os dados são estruturados em PostgreSQL
3. **Jupyter Notebook** lê da base estruturada, trata e treina um modelo
4. O modelo é versionado no **MLFlow** e exportado novamente para o S3
5. O **Dashboard** consome os dados e mostra visualizações e insights

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
