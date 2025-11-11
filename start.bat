@echo off
REM Script de inicialização do projeto para Windows
REM Uso: start.bat

echo ==========================================
echo Iniciando Projeto AV2 - Machine Learning
echo ==========================================
echo.

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Docker nao esta rodando. Por favor, inicie o Docker Desktop.
    pause
    exit /b 1
)

echo [OK] Docker esta rodando
echo.

REM Construir e iniciar os serviços
echo Construindo e iniciando os servicos...
docker-compose up -d --build

echo.
echo Aguardando servicos iniciarem...
timeout /t 10 /nobreak >nul

REM Verificar status
echo.
echo Status dos servicos:
docker-compose ps

echo.
echo ==========================================
echo Servicos disponiveis:
echo ==========================================
echo FastAPI:        http://localhost:8000
echo FastAPI Docs:   http://localhost:8000/docs
echo JupyterLab:     http://localhost:8888
echo MLFlow:         http://localhost:5000
echo MinIO Console:  http://localhost:9001
echo    (usuario: minioadmin, senha: minioadmin)
echo.
echo Para fazer upload do dataset:
echo   curl -X POST http://localhost:8000/upload -F "file=@Dataset of Diabetes .csv"
echo.
echo Para parar os servicos: docker-compose down
echo ==========================================
pause

