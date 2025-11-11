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
- **PostgreSQL** (Porta 5432): Banco de dados relacional para dados estruturados
- **JupyterLab** (Porta 8888): Ambiente de análise e modelagem
- **MLFlow** (Porta 5000): Rastreamento de experimentos e versionamento de modelos
- **Visualização**: Gráficos gerados nos notebooks e MLFlow UI

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
│   └── 02_preprocessing_and_modeling.ipynb
├── trendz/                     # Dashboards exportados
├── reports/                    # Figuras e plots dos resultados
├── Dataset of Diabetes .csv    # Dataset original
└── README.md                   # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose v2.0+
- 8GB+ de RAM disponível
- Portas 8000, 5000, 5432, 8888, 9000, 9001, 8080 disponíveis

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
- **JupyterLab**: http://localhost:8888
- **MLFlow**: http://localhost:5000
- **MinIO Console**: http://localhost:9001 (usuário: minioadmin, senha: minioadmin)

### Passo 6: Executar Análise

1. Acesse o JupyterLab em http://localhost:8888
2. Abra o notebook `notebooks/01_exploratory_data_analysis.ipynb`
3. Execute todas as células para análise exploratória
4. Abra o notebook `notebooks/02_preprocessing_and_modeling.ipynb`
5. Execute para treinar os modelos

## 📊 Dataset

O dataset contém:
- **1001 registros** de pacientes
- **13 features**: ID, No_Pation, Gender, AGE, Urea, Cr, HbA1c, Chol, TG, HDL, LDL, VLDL, BMI
- **Classe alvo**: CLASS (N=Non-diabetic, P=Prediabetic, Y=Diabetic)

## 🔬 Modelos Implementados

O projeto implementa e compara os seguintes algoritmos de classificação:

1. **Random Forest**
2. **Gradient Boosting**
3. **Support Vector Machine (SVM)**
4. **Logistic Regression**
5. **K-Nearest Neighbors (KNN)**

Todos os experimentos são registrados no MLFlow para comparação e versionamento.

## 📈 Métricas de Avaliação

- Accuracy (Acurácia)
- F1-Score (ponderado)
- Classification Report
- Confusion Matrix

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

1. **Balanceamento de dados**: Uso de SMOTE para lidar com desbalanceamento de classes
2. **Normalização**: StandardScaler para padronizar features
3. **Validação cruzada**: Para avaliação mais robusta
4. **MLFlow**: Rastreamento completo de experimentos
5. **Pipeline automatizado**: Integração completa entre componentes

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

- [Thiago von Sohsten] (@thiagovonsohsten)
- [Nome do membro 2] (@github_user2)
- [Nome do membro 3] (@github_user3)
- [Nome do membro 4] (@github_user4)
- [Nome do membro 5] (@github_user5)
- [Nome do membro 6] (@github_user6)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🎓 Instituição

**CESAR School**  
Disciplina: Aprendizado de Máquina - 2025.2  
Período: 2ª Unidade

---

**Nota**: Este projeto foi desenvolvido para fins acadêmicos como parte da avaliação da disciplina de Aprendizado de Máquina.
