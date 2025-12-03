# 📝 Como Criar Devices Manualmente no ThingsBoard

Como o tenant admin não tem permissão para criar devices via API, você precisa criá-los manualmente pela interface web.

## 🚀 Passo a Passo

### 1. Fazer Login como Tenant Admin

1. Acesse: http://localhost:8080
2. Faça logout se estiver logado como sysadmin
3. Faça login com:
   - **Email**: `admin@diabetes-ml.com`
   - **Senha**: `admin123`

### 2. Acessar Devices

1. No menu lateral, clique em **"Devices"**
2. Você verá a lista de devices (provavelmente vazia)

### 3. Criar Devices

Para cada modelo, crie um device:

#### Device 1: Model_Random_Forest
1. Clique no botão **"+"** (adicionar device)
2. Preencha:
   - **Name**: `Model_Random_Forest`
   - **Type**: `Diabetes Model` (ou deixe "default")
   - **Label**: `Random Forest Model`
3. Clique em **"Add"**

#### Device 2: Model_Gradient_Boosting
1. Clique no botão **"+"**
2. Preencha:
   - **Name**: `Model_Gradient_Boosting`
   - **Type**: `Diabetes Model`
   - **Label**: `Gradient Boosting Model`
3. Clique em **"Add"**

#### Device 3: Model_SVM
1. Clique no botão **"+"**
2. Preencha:
   - **Name**: `Model_SVM`
   - **Type**: `Diabetes Model`
   - **Label**: `SVM Model`
3. Clique em **"Add"**

#### Device 4: Model_KNN
1. Clique no botão **"+"**
2. Preencha:
   - **Name**: `Model_KNN`
   - **Type**: `Diabetes Model`
   - **Label**: `KNN Model`
3. Clique em **"Add"**

#### Device 5: Model_Logistic_Regression
1. Clique no botão **"+"**
2. Preencha:
   - **Name**: `Model_Logistic_Regression`
   - **Type**: `Diabetes Model`
   - **Label**: `Logistic Regression Model`
3. Clique em **"Add"**

#### Device 6: Dataset_Stats
1. Clique no botão **"+"**
2. Preencha:
   - **Name**: `Dataset_Stats`
   - **Type**: `Dataset Statistics`
   - **Label**: `Dataset Statistics`
3. Clique em **"Add"**

### 4. Verificar Devices Criados

Após criar todos os devices, você deve ver na lista:
- ✅ Model_Random_Forest
- ✅ Model_Gradient_Boosting
- ✅ Model_SVM
- ✅ Model_KNN
- ✅ Model_Logistic_Regression
- ✅ Dataset_Stats

### 5. Executar Script de Integração

Após criar os devices manualmente, o script de integração irá:
1. Encontrar os devices existentes
2. Enviar telemetria (métricas e predições) para eles

Execute:
```bash
docker-compose restart thingsboard_integration
```

Ou manualmente:
```bash
docker-compose exec thingsboard_integration python integrate_to_thingsboard.py
```

## ✅ Pronto!

Agora os devices estão criados e o script pode enviar dados para eles!

