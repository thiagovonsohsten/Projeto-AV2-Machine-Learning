"""
Dashboard Streamlit para Visualização de Resultados
Diabetes ML - Projeto AV2
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import os

# Tentar importar MLFlow (opcional)
try:
    from mlflow.tracking import MlflowClient
    MLFLOW_AVAILABLE = True
except:
    MLFLOW_AVAILABLE = False

# Configuração da página
st.set_page_config(
    page_title="Diabetes ML Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Conexão com PostgreSQL
@st.cache_resource
def get_db_connection():
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'diabetes_db')
    
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    return create_engine(DATABASE_URL)

# Conexão com MLFlow
@st.cache_resource
def get_mlflow_client():
    if MLFLOW_AVAILABLE:
        mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://mlflow:5000')
        try:
            return MlflowClient(mlflow_uri)
        except:
            return None
    return None

# Título principal
st.title("📊 Dashboard - Predição de Diabetes")
st.markdown("---")

# Sidebar
st.sidebar.title("Navegação")
page = st.sidebar.radio(
    "Selecione uma página:",
    ["📈 Visão Geral", "🔬 Análise de Dados", "🤖 Modelos ML", "📉 Métricas e Resultados"]
)

engine = get_db_connection()
mlflow_client = get_mlflow_client() if MLFLOW_AVAILABLE else None

# Página 1: Visão Geral
if page == "📈 Visão Geral":
    st.header("Visão Geral do Projeto")
    
    # Estatísticas do dataset
    try:
        query = "SELECT * FROM diabetes_processed"
        df = pd.read_sql(query, engine)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Registros", len(df))
        
        with col2:
            class_n = len(df[df['class_label'] == 'N'])
            st.metric("Não Diabéticos (N)", class_n)
        
        with col3:
            class_p = len(df[df['class_label'] == 'P'])
            st.metric("Pré-Diabéticos (P)", class_p)
        
        with col4:
            class_y = len(df[df['class_label'] == 'Y'])
            st.metric("Diabéticos (Y)", class_y)
        
        # Gráfico de distribuição de classes
        st.subheader("Distribuição de Classes")
        class_counts = df['class_label'].value_counts().sort_index()
        class_names = {'N': 'Não Diabético', 'P': 'Pré-Diabético', 'Y': 'Diabético'}
        class_counts_named = class_counts.rename(index=class_names)
        
        fig = px.pie(
            values=class_counts_named.values,
            names=class_counts_named.index,
            title="Distribuição de Classes no Dataset",
            color_discrete_map={
                'Não Diabético': '#2ecc71',
                'Pré-Diabético': '#f39c12',
                'Diabético': '#e74c3c'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas descritivas
        st.subheader("Estatísticas Descritivas")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in ['id', 'record_id', 'patient_number']]
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")

# Página 2: Análise de Dados
elif page == "🔬 Análise de Dados":
    st.header("Análise Exploratória dos Dados")
    
    try:
        query = "SELECT * FROM diabetes_processed"
        df = pd.read_sql(query, engine)
        
        # Seleção de variável
        st.subheader("Análise por Variável")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in ['id', 'record_id', 'patient_number']]
        
        selected_var = st.selectbox("Selecione uma variável:", numeric_cols)
        
        if selected_var:
            # Histograma por classe
            fig = px.histogram(
                df,
                x=selected_var,
                color='class_label',
                nbins=30,
                title=f"Distribuição de {selected_var.upper()} por Classe",
                labels={'class_label': 'Classe'},
                color_discrete_map={'N': '#2ecc71', 'P': '#f39c12', 'Y': '#e74c3c'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Boxplot
            fig2 = px.box(
                df,
                x='class_label',
                y=selected_var,
                title=f"Boxplot de {selected_var.upper()} por Classe",
                color='class_label',
                color_discrete_map={'N': '#2ecc71', 'P': '#f39c12', 'Y': '#e74c3c'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Matriz de correlação
        st.subheader("Matriz de Correlação")
        corr_cols = ['age', 'urea', 'creatinine', 'hba1c', 'cholesterol', 
                     'triglycerides', 'hdl', 'ldl', 'vldl', 'bmi']
        corr_cols = [col for col in corr_cols if col in df.columns]
        
        if corr_cols:
            corr_matrix = df[corr_cols].corr()
            fig3 = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Matriz de Correlação",
                color_continuous_scale="RdBu"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")

# Página 3: Modelos ML
elif page == "🤖 Modelos ML":
    st.header("Modelos de Machine Learning")
    
    try:
        # Buscar métricas do banco
        query = "SELECT * FROM model_metrics ORDER BY accuracy DESC"
        metrics_df = pd.read_sql(query, engine)
        
        if not metrics_df.empty:
            st.subheader("Comparação de Modelos")
            
            # Tabela de métricas
            st.dataframe(metrics_df[['model_name', 'accuracy', 'f1_score_weighted', 'f1_score_macro']], 
                        use_container_width=True)
            
            # Gráfico de comparação
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=metrics_df['model_name'],
                y=metrics_df['accuracy'],
                name='Accuracy',
                marker_color='#3498db'
            ))
            
            fig.add_trace(go.Bar(
                x=metrics_df['model_name'],
                y=metrics_df['f1_score_weighted'],
                name='F1-Score (weighted)',
                marker_color='#2ecc71'
            ))
            
            fig.add_trace(go.Bar(
                x=metrics_df['model_name'],
                y=metrics_df['f1_score_macro'],
                name='F1-Score (macro)',
                marker_color='#e74c3c'
            ))
            
            fig.update_layout(
                title="Comparação de Performance dos Modelos",
                xaxis_title="Modelo",
                yaxis_title="Score",
                barmode='group',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Melhor modelo
            best_model = metrics_df.iloc[0]
            st.success(f"🏆 Melhor Modelo: **{best_model['model_name']}** com Accuracy de {best_model['accuracy']:.4f}")
        else:
            st.warning("Nenhuma métrica de modelo encontrada. Execute o notebook de modelagem primeiro.")
        
        # Informações do MLFlow
        st.subheader("Experimentos no MLFlow")
        if mlflow_client:
            try:
                experiments = mlflow_client.search_experiments()
                if experiments:
                    for exp in experiments[:5]:  # Mostrar até 5 experimentos
                        with st.expander(f"Experimento: {exp.name}"):
                            runs = mlflow_client.search_runs(experiment_ids=[exp.experiment_id], max_results=5)
                            for run in runs:
                                st.write(f"**Run:** {run.info.run_name}")
                                st.write(f"Accuracy: {run.data.metrics.get('accuracy', 'N/A')}")
                                st.write(f"F1-Score: {run.data.metrics.get('f1_score_weighted', 'N/A')}")
                else:
                    st.info("Nenhum experimento encontrado no MLFlow")
            except Exception as e:
                st.warning(f"Não foi possível conectar ao MLFlow: {str(e)}")
        else:
            st.info("MLFlow não disponível. Acesse http://localhost:5000 para ver os experimentos.")
            
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")

# Página 4: Métricas e Resultados
elif page == "📉 Métricas e Resultados":
    st.header("Métricas Detalhadas e Resultados")
    
    try:
        query = "SELECT * FROM model_metrics ORDER BY accuracy DESC"
        metrics_df = pd.read_sql(query, engine)
        
        if not metrics_df.empty:
            # Selecionar modelo
            selected_model = st.selectbox("Selecione um modelo:", metrics_df['model_name'].unique())
            
            model_metrics = metrics_df[metrics_df['model_name'] == selected_model].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Accuracy", f"{model_metrics['accuracy']:.4f}")
            
            with col2:
                st.metric("F1-Score (weighted)", f"{model_metrics['f1_score_weighted']:.4f}")
            
            with col3:
                st.metric("F1-Score (macro)", f"{model_metrics['f1_score_macro']:.4f}")
            
            # Métricas por classe
            st.subheader("Métricas por Classe")
            
            metrics_by_class = pd.DataFrame({
                'Classe': ['N (Não Diabético)', 'P (Pré-Diabético)', 'Y (Diabético)'],
                'Precision': [
                    model_metrics['precision_n'],
                    model_metrics['precision_p'],
                    model_metrics['precision_y']
                ],
                'Recall': [
                    model_metrics['recall_n'],
                    model_metrics['recall_p'],
                    model_metrics['recall_y']
                ]
            })
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Precision',
                x=metrics_by_class['Classe'],
                y=metrics_by_class['Precision'],
                marker_color='#3498db'
            ))
            
            fig.add_trace(go.Bar(
                name='Recall',
                x=metrics_by_class['Classe'],
                y=metrics_by_class['Recall'],
                marker_color='#2ecc71'
            ))
            
            fig.update_layout(
                title=f"Métricas por Classe - {selected_model}",
                xaxis_title="Classe",
                yaxis_title="Score",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Predições recentes
            st.subheader("Predições Recentes")
            # Buscar predições - primeiro tenta nome exato, depois busca por nome base (ex: "Gradient Boosting" vs "Gradient Boosting - Optimized")
            base_model_name = selected_model.split(' - ')[0]  # Remove sufixos como "- Optimized"
            pred_query = text("""
                SELECT * FROM model_predictions 
                WHERE model_name = :model_name 
                   OR model_name = :base_name
                   OR model_name LIKE :pattern 
                ORDER BY created_at DESC 
                LIMIT 100
            """)
            predictions_df = pd.read_sql(pred_query, engine, params={
                'model_name': selected_model, 
                'base_name': base_model_name,
                'pattern': f'{base_model_name}%'
            })
            
            if not predictions_df.empty:
                st.dataframe(predictions_df, use_container_width=True)
            else:
                st.info("Nenhuma predição encontrada para este modelo")
        else:
            st.warning("Execute o notebook de modelagem para ver as métricas")
            
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Projeto AV2 - Machine Learning | CESAR School 2025.2**")

