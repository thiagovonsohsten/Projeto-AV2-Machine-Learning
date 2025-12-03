# 🔗 Integração ThingsBoard - Projeto Diabetes ML

Este diretório contém o script de integração que sincroniza dados do PostgreSQL para o ThingsBoard, permitindo visualização em dashboards interativos.

## 📋 Arquivos

- `integrate_to_thingsboard.py`: Script principal de integração
- `requirements.txt`: Dependências Python
- `Dockerfile`: Imagem Docker para execução automática
- `GUIA_DASHBOARD_THINGSBOARD.md`: Guia completo de configuração

## 🚀 Uso

### Execução Manual

```bash
cd thingsboard
pip install -r requirements.txt
python integrate_to_thingsboard.py
```

### Execução via Docker Compose

O serviço `thingsboard_integration` no `docker-compose.yml` executa automaticamente a cada 5 minutos.

```bash
docker-compose up -d thingsboard_integration
```

## 🔧 O que o script faz

1. **Login no ThingsBoard**: Autentica usando credenciais configuradas
2. **Cria dispositivos**: Um device para cada modelo de ML e um para estatísticas
3. **Sincroniza métricas**: Envia métricas dos modelos (accuracy, F1-score, precision, recall)
4. **Sincroniza predições**: Envia contagens e distribuições de predições
5. **Sincroniza estatísticas**: Envia estatísticas do dataset
6. **Cria dashboard**: Cria um dashboard básico (widgets devem ser configurados manualmente)

## 📊 Dados Sincronizados

### Dispositivos Criados

- `Model_Random_Forest`
- `Model_Gradient_Boosting`
- `Model_SVM`
- `Model_KNN`
- `Model_Logistic_Regression`
- `Dataset_Stats`

### Telemetria Enviada

**Para cada modelo:**
- `accuracy`: Acurácia do modelo
- `f1_score_weighted`: F1-Score ponderado
- `f1_score_macro`: F1-Score macro
- `precision_n`, `precision_p`, `precision_y`: Precisão por classe
- `recall_n`, `recall_p`, `recall_y`: Recall por classe
- `predictions_count`: Número de predições
- `avg_confidence`: Confiança média
- `class_n_count`, `class_p_count`, `class_y_count`: Contagem por classe

**Para Dataset_Stats:**
- `total_records`: Total de registros
- `class_n_count`, `class_p_count`, `class_y_count`: Distribuição de classes
- `avg_age`, `avg_hba1c`, `avg_bmi`: Médias de features importantes

## 📖 Próximos Passos

Após executar o script, siga o guia em `GUIA_DASHBOARD_THINGSBOARD.md` para:
1. Configurar widgets no dashboard
2. Personalizar visualizações
3. Organizar layout
4. Configurar alertas

## 🔄 Atualização Automática

O script executa automaticamente a cada 5 minutos quando rodando via Docker Compose.

Para atualizar manualmente:

```bash
docker-compose restart thingsboard_integration
```

## 🐛 Troubleshooting

### Erro de conexão

Verifique se o ThingsBoard está rodando:
```bash
docker-compose ps thingsboard
```

### Dados não aparecem

1. Verifique se há dados no PostgreSQL:
   ```bash
   docker-compose exec postgres psql -U postgres -d diabetes_db -c "SELECT COUNT(*) FROM model_metrics;"
   ```

2. Execute o script manualmente para ver logs detalhados:
   ```bash
   docker-compose exec thingsboard_integration python integrate_to_thingsboard.py
   ```

## 📝 Variáveis de Ambiente

- `THINGSBOARD_URL`: URL do ThingsBoard (padrão: `http://thingsboard:9090` no Docker, `http://localhost:8080` local)
- `THINGSBOARD_USERNAME`: Usuário do ThingsBoard (padrão: `sysadmin@thingsboard.org`)
- `THINGSBOARD_PASSWORD`: Senha do ThingsBoard (padrão: `sysadmin`)
- `POSTGRES_HOST`: Host do PostgreSQL (padrão: `postgres`)
- `POSTGRES_PORT`: Porta do PostgreSQL (padrão: `5432`)
- `POSTGRES_USER`: Usuário do PostgreSQL (padrão: `postgres`)
- `POSTGRES_PASSWORD`: Senha do PostgreSQL (padrão: `postgres`)
- `POSTGRES_DB`: Nome do banco (padrão: `diabetes_db`)

