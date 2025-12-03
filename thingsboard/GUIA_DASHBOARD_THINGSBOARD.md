# 🎯 Guia de Configuração do Dashboard ThingsBoard

## 📋 Visão Geral

Este guia explica como configurar dashboards interativos no ThingsBoard para visualizar resultados e predições do projeto de Machine Learning de Diabetes.

---

## ✅ Pré-requisitos

1. **ThingsBoard rodando** em http://localhost:8080
2. **Login realizado** com credenciais: `sysadmin@thingsboard.org` / `sysadmin`
3. **Script de integração executado** (dados sincronizados)

---

## 🚀 Passo 1: Executar Integração de Dados

O script de integração sincroniza automaticamente os dados do PostgreSQL para o ThingsBoard.

### Opção A: Via Docker Compose (Automático)

O serviço `thingsboard_integration` no `docker-compose.yml` executa automaticamente a cada 5 minutos.

```bash
docker-compose up -d thingsboard_integration
```

### Opção B: Execução Manual

```bash
cd thingsboard
python integrate_to_thingsboard.py
```

### O que o script faz:

1. ✅ Cria dispositivos (devices) para cada modelo
2. ✅ Cria dispositivo para estatísticas do dataset
3. ✅ Envia métricas dos modelos como telemetria
4. ✅ Envia predições como telemetria
5. ✅ Cria dashboard básico

---

## 📊 Passo 2: Acessar o ThingsBoard

1. Abra o navegador em: **http://localhost:8080**
2. Faça login com:
   - **Usuário**: `sysadmin@thingsboard.org`
   - **Senha**: `sysadmin`

---

## 🔧 Passo 3: Verificar Dispositivos Criados

1. No menu lateral, clique em **Devices** → **All**
2. Você verá dispositivos como:
   - `Model_Random_Forest`
   - `Model_Gradient_Boosting`
   - `Model_SVM`
   - `Model_KNN`
   - `Model_Logistic_Regression`
   - `Dataset_Stats`

3. Clique em um dispositivo para ver:
   - **Latest Telemetry**: Últimos valores enviados
   - **Attributes**: Atributos do dispositivo
   - **Relations**: Relações com outros dispositivos

---

## 🎨 Passo 4: Criar/Editar Dashboard

### 4.1. Criar Novo Dashboard

1. No menu lateral, clique em **Dashboards** → **+** (adicionar)
2. Nome: `Diabetes ML Dashboard`
3. Clique em **Add**

### 4.2. Editar Dashboard

1. Abra o dashboard criado
2. Clique no botão **Edit** (canto superior direito)
3. O dashboard entrará em modo de edição

---

## 📈 Passo 5: Adicionar Widgets

### Widget 1: Cards de Métricas dos Modelos

**Objetivo**: Exibir Accuracy e F1-Score de cada modelo

1. Clique em **+** (adicionar widget)
2. Escolha **Cards** → **Latest values**
3. Configure:
   - **Data source**: Selecione um device (ex: `Model_Random_Forest`)
   - **Keys**: Selecione `accuracy` e `f1_score_weighted`
   - **Card settings**: Personalize cores e labels
4. Clique em **Add**

**Repita para cada modelo!**

### Widget 2: Gráfico de Comparação de Modelos

**Objetivo**: Comparar Accuracy de todos os modelos

1. Clique em **+** → **Charts** → **Timeseries line chart**
2. Configure:
   - **Data source**: Selecione múltiplos devices (todos os modelos)
   - **Keys**: Selecione `accuracy` para todos
   - **Time window**: Últimas 24 horas
3. Clique em **Add**

### Widget 3: Distribuição de Classes (Pizza)

**Objetivo**: Mostrar distribuição de predições (N, P, Y)

1. Clique em **+** → **Charts** → **Pie chart**
2. Configure:
   - **Data source**: Selecione um device de modelo
   - **Keys**: `class_n_count`, `class_p_count`, `class_y_count`
3. Clique em **Add**

### Widget 4: Tabela de Métricas Detalhadas

**Objetivo**: Tabela com todas as métricas

1. Clique em **+** → **Tables** → **Latest values table**
2. Configure:
   - **Data source**: Selecione todos os devices de modelos
   - **Keys**: Selecione todas as métricas:
     - `accuracy`
     - `f1_score_weighted`
     - `f1_score_macro`
     - `precision_n`, `precision_p`, `precision_y`
     - `recall_n`, `recall_p`, `recall_y`
3. Clique em **Add**

### Widget 5: Estatísticas do Dataset

**Objetivo**: Exibir estatísticas gerais do dataset

1. Clique em **+** → **Cards** → **Latest values**
2. Configure:
   - **Data source**: `Dataset_Stats`
   - **Keys**: 
     - `total_records`
     - `class_n_count`
     - `class_p_count`
     - `class_y_count`
     - `avg_age`
     - `avg_hba1c`
     - `avg_bmi`
3. Clique em **Add**

### Widget 6: Gráfico de Predições ao Longo do Tempo

**Objetivo**: Visualizar predições ao longo do tempo

1. Clique em **+** → **Charts** → **Timeseries line chart**
2. Configure:
   - **Data source**: Selecione um device de modelo
   - **Keys**: `predictions_count`
   - **Time window**: Últimas 24 horas
   - **Aggregation**: COUNT
3. Clique em **Add**

### Widget 7: Confiança das Predições

**Objetivo**: Mostrar confiança média das predições

1. Clique em **+** → **Charts** → **Timeseries line chart**
2. Configure:
   - **Data source**: Selecione um device de modelo
   - **Keys**: `avg_confidence`
   - **Time window**: Últimas 24 horas
3. Clique em **Add**

---

## 🎯 Passo 6: Organizar Layout do Dashboard

1. **Arraste e solte** os widgets para reorganizar
2. **Redimensione** os widgets clicando e arrastando as bordas
3. **Configure o layout**:
   - Clique em **Settings** (ícone de engrenagem)
   - Ajuste **Grid settings** para melhor organização
   - Configure **Mobile layout** se necessário

---

## 💾 Passo 7: Salvar Dashboard

1. Após configurar todos os widgets, clique em **Save** (canto superior direito)
2. O dashboard será salvo e estará disponível para visualização

---

## 🔄 Passo 8: Atualização Automática

O script de integração executa automaticamente a cada 5 minutos, atualizando os dados no ThingsBoard.

Para atualizar manualmente:

```bash
docker-compose restart thingsboard_integration
```

---

## 📱 Passo 9: Visualizar Dashboard

1. No menu lateral, clique em **Dashboards**
2. Selecione **Diabetes ML Dashboard**
3. O dashboard exibirá:
   - ✅ Métricas dos modelos em tempo real
   - ✅ Predições e distribuições
   - ✅ Estatísticas do dataset
   - ✅ Gráficos interativos

---

## 🎨 Dicas de Personalização

### Cores e Estilo

1. Clique em um widget → **Edit**
2. Vá em **Advanced** → **Color settings**
3. Personalize cores, gradientes e transparências

### Filtros de Tempo

1. No topo do dashboard, configure o **Time window**
2. Escolha entre:
   - **Realtime**: Dados em tempo real
   - **History**: Dados históricos com intervalo configurável

### Alertas

1. Configure **Alarm rules** nos devices
2. Crie alertas para:
   - Accuracy abaixo de um threshold
   - Confiança baixa nas predições
   - Erros no modelo

---

## ✅ Checklist de Configuração

- [ ] ThingsBoard acessível em http://localhost:8080
- [ ] Login realizado com sucesso
- [ ] Script de integração executado
- [ ] Dispositivos criados e visíveis
- [ ] Dashboard criado
- [ ] Widgets adicionados ao dashboard
- [ ] Layout organizado
- [ ] Dashboard salvo
- [ ] Dados sendo atualizados automaticamente

---

## 🐛 Troubleshooting

### Problema: Dispositivos não aparecem

**Solução**: Execute o script de integração manualmente:
```bash
cd thingsboard
python integrate_to_thingsboard.py
```

### Problema: Widgets não exibem dados

**Solução**: 
1. Verifique se o device tem telemetria (Latest Telemetry)
2. Verifique se as keys estão corretas
3. Ajuste o Time window do widget

### Problema: Dados não atualizam

**Solução**: 
1. Verifique se o serviço `thingsboard_integration` está rodando:
   ```bash
   docker-compose ps thingsboard_integration
   ```
2. Reinicie o serviço:
   ```bash
   docker-compose restart thingsboard_integration
   ```

---

## 🎉 Pronto!

Agora você tem:
- ✅ **ThingsBoard** (porta 8080) com dashboards interativos
- ✅ **Trendz Analytics** (porta 8888) com visualizações
- ✅ Dados sincronizados automaticamente
- ✅ Visualizações em tempo real

**Acesse:**
- ThingsBoard: http://localhost:8080
- Trendz Analytics: http://localhost:8888

