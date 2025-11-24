# 🚀 Guia Rápido de Teste

## ⚠️ Problema Comum: Docker Desktop não está rodando

Se você recebeu o erro:
```
The system cannot find the file specified
```

**Solução**: O Docker Desktop precisa estar rodando!

### Passo 1: Verificar Docker Desktop

1. Abra o **Docker Desktop** no Windows
2. Aguarde até aparecer "Docker Desktop is running" na barra de tarefas
3. Verifique se está rodando:
   ```powershell
   docker --version
   docker-compose --version
   ```

Se não tiver o Docker Desktop instalado:
- Baixe em: https://www.docker.com/products/docker-desktop/
- Instale e reinicie o computador

---

## 📋 Passo a Passo para Testar

### 1️⃣ Iniciar Docker Desktop
- Abra o Docker Desktop
- Aguarde até ficar verde/ativo

### 2️⃣ Abrir PowerShell no diretório do projeto
```powershell
cd C:\Users\thiag\Desktop\Projeto-AV2-Machine-Learning
```

### 3️⃣ Iniciar os serviços
```powershell
docker-compose up -d
```

**Aguarde alguns minutos** enquanto as imagens são baixadas (primeira vez é mais lento).

### 4️⃣ Verificar se tudo está rodando
```powershell
docker-compose ps
```

Você deve ver algo como:
```
NAME                STATUS
fastapi_ingestion   Up
jupyterlab          Up
mlflow              Up
minio               Up (healthy)
postgres_db         Up (healthy)
```

### 5️⃣ Fazer upload do dataset

**Opção A - Script Python (Recomendado):**
```powershell
# Instalar requests se necessário
pip install requests

# Executar upload
python upload_dataset.py
```

**Opção B - Via navegador:**
1. Abra: http://localhost:8000/docs
2. Clique em `/upload` → `Try it out`
3. Selecione o arquivo `Dataset of Diabetes .csv`
4. Clique em `Execute`

**Opção C - PowerShell:**
```powershell
curl.exe -X POST "http://localhost:8000/upload" -F "file=@Dataset of Diabetes .csv"
```

### 6️⃣ Acessar os serviços

Abra no navegador:

- ✅ **FastAPI Docs**: http://localhost:8000/docs
- ✅ **JupyterLab**: http://localhost:8888
- ✅ **MLFlow**: http://localhost:5000
- ✅ **MinIO Console**: http://localhost:9001
  - Usuário: `minioadmin`
  - Senha: `minioadmin`

### 7️⃣ Executar análise no JupyterLab

1. Acesse http://localhost:8888
2. Abra `notebooks/01_exploratory_data_analysis.ipynb`
3. Execute todas as células (Shift + Enter)
4. Depois abra `notebooks/02_preprocessing_and_modeling.ipynb`
5. Execute para treinar os modelos

---

## 🔍 Verificar se está funcionando

### Testar API:
```powershell
# Verificar saúde dos serviços
curl http://localhost:8000/health

# Ver estatísticas (após upload)
curl http://localhost:8000/data/stats
```

### Ver logs de um serviço:
```powershell
docker-compose logs -f fastapi
docker-compose logs -f jupyterlab
```

### Parar tudo:
```powershell
docker-compose down
```

### Reiniciar um serviço específico:
```powershell
docker-compose restart fastapi
```

---

## ❌ Problemas Comuns

### Erro: "Port already in use"
Alguma porta está sendo usada. Verifique:
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :8888
```

### Erro: "Cannot connect to Docker daemon"
- Docker Desktop não está rodando
- Reinicie o Docker Desktop

### Erro: "No space left on device"
- Limpe imagens antigas:
```powershell
docker system prune -a
```

### Serviço não inicia
Ver logs:
```powershell
docker-compose logs <nome-do-servico>
```

---

## ✅ Checklist de Teste

- [ ] Docker Desktop está rodando
- [ ] `docker-compose up -d` executado com sucesso
- [ ] Todos os serviços estão "Up" (verificar com `docker-compose ps`)
- [ ] Upload do dataset realizado
- [ ] API responde em http://localhost:8000/docs
- [ ] JupyterLab abre em http://localhost:8888
- [ ] MLFlow abre em http://localhost:5000
- [ ] Notebooks executam sem erros

---

## 📞 Próximos Passos

Após tudo funcionando:
1. Execute a análise exploratória no notebook 01
2. Execute o treinamento de modelos no notebook 02
3. Visualize os resultados no MLFlow
4. Veja os gráficos salvos em `reports/`

