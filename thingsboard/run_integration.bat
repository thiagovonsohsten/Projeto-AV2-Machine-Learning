@echo off
REM Script para executar integração ThingsBoard uma vez (Windows)

echo 🔗 Executando integração ThingsBoard...

REM Verificar se está dentro do Docker ou localmente
if exist "C:\\.dockerenv" (
    REM Dentro do Docker
    python integrate_to_thingsboard.py
) else (
    REM Localmente - usar localhost
    set THINGSBOARD_URL=http://localhost:8080
    python integrate_to_thingsboard.py
)

