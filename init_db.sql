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

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_diabetes_class ON diabetes_processed(class_label);
CREATE INDEX IF NOT EXISTS idx_diabetes_age ON diabetes_processed(age);
CREATE INDEX IF NOT EXISTS idx_predictions_model ON model_predictions(model_name);

