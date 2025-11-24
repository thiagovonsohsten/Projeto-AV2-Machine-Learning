# 📊 Guia do Dashboard

## Dashboard Streamlit (Recomendado)

O dashboard principal está disponível em **http://localhost:8501**

### Funcionalidades:

1. **📈 Visão Geral**
   - Estatísticas do dataset
   - Distribuição de classes
   - Métricas descritivas

2. **🔬 Análise de Dados**
   - Análise por variável (histogramas, boxplots)
   - Matriz de correlação interativa
   - Visualizações dinâmicas

3. **🤖 Modelos ML**
   - Comparação de modelos
   - Métricas de performance
   - Integração com MLFlow

4. **📉 Métricas e Resultados**
   - Métricas detalhadas por modelo
   - Métricas por classe (Precision, Recall)
   - Predições recentes

### Como Usar:

1. Execute o notebook `04_export_to_dashboard.ipynb` para exportar dados
2. Acesse http://localhost:8501
3. Navegue pelas páginas usando o menu lateral

## ThingsBoard (Opcional)

ThingsBoard está disponível em **http://localhost:8080**

### Credenciais Padrão:
- **Usuário**: tenant@thingsboard.org
- **Senha**: tenant

### Configuração:

1. Acesse http://localhost:8080
2. Faça login com as credenciais acima
3. Crie dispositivos e dashboards conforme necessário
4. Configure widgets para visualizar dados do PostgreSQL

### Nota:

O ThingsBoard pode demorar alguns minutos para iniciar completamente. Se não funcionar, use o Dashboard Streamlit que é mais rápido e já está configurado.

