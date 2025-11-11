FROM jupyter/scipy-notebook:latest

USER root

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER jovyan

# Instalar pacotes Python adicionais
RUN pip install --no-cache-dir \
    mlflow==2.8.1 \
    boto3==1.29.7 \
    psycopg2-binary==2.9.9 \
    sqlalchemy==2.0.23 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    pandas==2.1.3 \
    numpy==1.26.2 \
    plotly==5.18.0 \
    imbalanced-learn==0.11.0 \
    jupyterlab==4.0.9

# Criar diretórios de trabalho
RUN mkdir -p /home/jovyan/work/notebooks \
    && mkdir -p /home/jovyan/work/reports

WORKDIR /home/jovyan/work

