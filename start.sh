#!/bin/bash

# Script de inicialização do projeto
# Uso: ./start.sh

echo "=========================================="
echo "Iniciando Projeto AV2 - Machine Learning"
echo "=========================================="
echo ""

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker Desktop."
    exit 1
fi

echo "✅ Docker está rodando"
echo ""

# Construir e iniciar os serviços
echo "Construindo e iniciando os serviços..."
docker-compose up -d --build

echo ""
echo "Aguardando serviços iniciarem..."
sleep 10

# Verificar status
echo ""
echo "Status dos serviços:"
docker-compose ps

echo ""
echo "=========================================="
echo "Serviços disponíveis:"
echo "=========================================="
echo "📊 FastAPI:        http://localhost:8000"
echo "📚 FastAPI Docs:   http://localhost:8000/docs"
echo "🔬 JupyterLab:     http://localhost:8888"
echo "📈 MLFlow:         http://localhost:5000"
echo "💾 MinIO Console:  http://localhost:9001"
echo "   (usuário: minioadmin, senha: minioadmin)"
echo ""
echo "Para fazer upload do dataset:"
echo "  curl -X POST http://localhost:8000/upload -F \"file=@Dataset of Diabetes .csv\""
echo ""
echo "Para parar os serviços: docker-compose down"
echo "=========================================="

