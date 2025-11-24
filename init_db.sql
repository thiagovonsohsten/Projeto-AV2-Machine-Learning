-- Script de inicialização do banco de dados PostgreSQL
-- Cria tabelas para armazenar dados tratados

-- Tabela para dados de diabetes processados
CREATE TABLE IF NOT EXISTS diabetes_processed (
    id SERIAL PRIMARY KEY,
    record_id INTEGER,
    patient_number INTEGER,
    gender VARCHAR(1),
    age INTEGER,
    urea FLOAT,
    creatinine FLOAT,
    hba1c FLOAT,
    cholesterol FLOAT,
    triglycerides FLOAT,
    hdl FLOAT,
    ldl FLOAT,
    vldl FLOAT,
    bmi FLOAT,
    class_label VARCHAR(1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para armazenar resultados de modelos
CREATE TABLE IF NOT EXISTS model_predictions (
    id SERIAL PRIMARY KEY,
    record_id INTEGER,
    predicted_class VARCHAR(1),
    confidence_score FLOAT,
    model_name VARCHAR(255),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para métricas de modelos (para dashboard)
CREATE TABLE IF NOT EXISTS model_metrics (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255),
    accuracy FLOAT,
    f1_score_weighted FLOAT,
    f1_score_macro FLOAT,
    precision_n FLOAT,
    precision_p FLOAT,
    precision_y FLOAT,
    recall_n FLOAT,
    recall_p FLOAT,
    recall_y FLOAT,
    mlflow_run_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para estatísticas do dataset (para dashboard)
CREATE TABLE IF NOT EXISTS dataset_stats (
    id SERIAL PRIMARY KEY,
    total_records INTEGER,
    class_n_count INTEGER,
    class_p_count INTEGER,
    class_y_count INTEGER,
    avg_age FLOAT,
    avg_hba1c FLOAT,
    avg_bmi FLOAT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_diabetes_class ON diabetes_processed(class_label);
CREATE INDEX IF NOT EXISTS idx_diabetes_age ON diabetes_processed(age);
CREATE INDEX IF NOT EXISTS idx_predictions_model ON model_predictions(model_name);
CREATE INDEX IF NOT EXISTS idx_model_metrics_name ON model_metrics(model_name);

