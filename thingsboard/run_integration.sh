#!/bin/bash
# Script para executar integração ThingsBoard uma vez

echo "🔗 Executando integração ThingsBoard..."

# Verificar se está dentro do Docker ou localmente
if [ -f /.dockerenv ]; then
    # Dentro do Docker
    python integrate_to_thingsboard.py
else
    # Localmente - usar localhost
    export THINGSBOARD_URL="http://localhost:8080"
    python integrate_to_thingsboard.py
fi

