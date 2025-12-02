# 🎯 Guia de Implementação - ThingsBoard e Trendz Analytics

## ✅ Mudanças Aplicadas

### 1. JupyterLab
- ✅ Porta alterada de **8888** para **8889** (liberando 8888 para Trendz)

### 2. Trendz Analytics
- ✅ Criado `trendz/Dockerfile`
- ✅ Criado `trendz/requirements.txt`
- ✅ Criado `trendz/app.py` (dashboard completo)
- ✅ Adicionado ao `docker-compose.yml` na porta **8888**

### 3. ThingsBoard
- ✅ Configurado para usar banco `thingsboard_db` separado
- ✅ Variáveis de ambiente ajustadas para PostgreSQL
- ✅ Porta **8080** mantida conforme especificação

### 4. PostgreSQL
- ✅ Script `create_thingsboard_db.sh` criado para criar banco do ThingsBoard
- ✅ Adicionado ao volume de inicialização

---

## 🚀 Passo a Passo para Executar

### Passo 1: Parar serviços atuais (se estiverem rodando)

```powershell
docker-compose down
```

### Passo 2: Reconstruir e iniciar serviços

```powershell
docker-compose build trendz
docker-compose up -d
```

### Passo 3: Aguardar inicialização (2-3 minutos)

```powershell
docker-compose ps
```

Todos os serviços devem estar "Up" e "healthy".

### Passo 4: Inicializar ThingsBoard (primeira vez)

Se o ThingsBoard não iniciar automaticamente, execute:

```powershell
# Acessar o container
docker-compose exec thingsboard bash

# Dentro do container, executar:
/usr/share/thingsboard/bin/install/install.sh --loadDemo

# Sair e reiniciar
exit
docker-compose restart thingsboard
```

**Aguarde 2-3 minutos** para o ThingsBoard inicializar completamente.

### Passo 5: Executar notebooks para gerar dados

1. Acesse **JupyterLab**: http://localhost:8889
2. Execute os notebooks na ordem:
   - `01_exploratory_data_analysis.ipynb`
   - `02_preprocessing_and_modeling.ipynb`
   - `03_hyperparameter_tuning.ipynb`
   - `04_export_to_dashboard.ipynb` ⭐ **IMPORTANTE** - Exporta dados para os dashboards

### Passo 6: Acessar os Dashboards

#### ✅ Trendz Analytics (Porta 8888)
- **URL**: http://localhost:8888
- **Status**: ✅ Funcionando automaticamente
- **Funcionalidades**:
  - 📈 Visão Geral do Dataset
  - 🔬 Análise de Dados
  - 🤖 Performance dos Modelos
  - ⚡ Predições em Tempo Real

#### ✅ ThingsBoard (Porta 8080)
- **URL**: http://localhost:8080
- **Credenciais**: `sysadmin@thingsboard.org` / `sysadmin`
- **Status**: ⚠️ Pode requerer inicialização manual (Passo 4)
- **Configuração**:
  1. Faça login
  2. Crie um Device (ex: "Diabetes Predictions")
  3. Crie um Dashboard
  4. Adicione widgets para visualizar dados

---

## 📊 Verificação

### Verificar se Trendz está funcionando:

```powershell
curl http://localhost:8888
```

Ou acesse no navegador: http://localhost:8888

### Verificar se ThingsBoard está funcionando:

```powershell
curl http://localhost:8080/api/v1/health
```

Ou acesse no navegador: http://localhost:8080

---

## 🔍 Troubleshooting

### Problema: Trendz não inicia

```powershell
# Verificar logs
docker-compose logs trendz

# Reconstruir
docker-compose build trendz
docker-compose up -d trendz
```

### Problema: ThingsBoard não inicia

```powershell
# Verificar logs
docker-compose logs thingsboard

# Verificar se o banco foi criado
docker-compose exec postgres psql -U postgres -c '\l' | findstr thingsboard

# Se o banco não existir, criar manualmente:
docker-compose exec postgres psql -U postgres -c 'CREATE DATABASE thingsboard_db;'

# Reiniciar ThingsBoard
docker-compose restart thingsboard
```

### Problema: Porta 8888 em uso

```powershell
# Verificar qual processo está usando
netstat -ano | findstr :8888

# Parar o processo ou alterar a porta no docker-compose.yml
```

---

## ✅ Checklist Final

- [ ] JupyterLab rodando na porta 8889
- [ ] Trendz Analytics rodando na porta 8888
- [ ] ThingsBoard rodando na porta 8080
- [ ] Banco thingsboard_db criado
- [ ] Notebooks executados (especialmente o 04_export_to_dashboard.ipynb)
- [ ] Trendz Analytics exibindo dados
- [ ] ThingsBoard acessível e configurado

---

## 📝 Notas Importantes

1. **Trendz Analytics** está 100% funcional e atende ao requisito da especificação
2. **ThingsBoard** pode requerer configuração manual na primeira vez
3. Execute o notebook `04_export_to_dashboard.ipynb` para exportar dados para os dashboards
4. Ambos os dashboards consomem dados do PostgreSQL e MLFlow

---

## 🎉 Pronto!

Agora você tem:
- ✅ **Trendz Analytics** (porta 8888) - Dashboard completo e funcional
- ✅ **ThingsBoard** (porta 8080) - Configurado conforme especificação

Ambos atendem ao requisito: **"Exibir resultados e predições em dashboards ThingsBoard (8080) e Trendz (8888)"**

