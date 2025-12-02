"""
Trendz Analytics - Dashboard de Visualização e Análise de Resultados ML
Diabetes ML - Projeto AV2
Porta 8888 conforme especificação
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
    page_title="Trendz Analytics - Predição de Diabetes",
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
st.title("📊 Trendz Analytics - Predição de Diabetes")
st.markdown("**Dashboard de Visualização e Análise de Resultados ML**")
st.markdown("---")

# Sidebar
st.sidebar.title("Navegação Trendz")
page = st.sidebar.radio(
    "Selecione uma página:",
    ["📈 Visão Geral", "🔬 Análise de Dados", "🤖 Performance dos Modelos", "⚡ Predições em Tempo Real"]
)

engine = get_db_connection()
mlflow_client = get_mlflow_client() if MLFLOW_AVAILABLE else None

# Página 1: Visão Geral
if page == "📈 Visão Geral":
    st.header("Visão Geral do Dataset")
    
    # Estatísticas do dataset
    try:
        # Buscar estatísticas do dataset
        stats_query = "SELECT * FROM dataset_stats LIMIT 1"
        stats_df = pd.read_sql(stats_query, engine)
        
        if not stats_df.empty:
            stats = stats_df.iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Idade Média", f"{stats.get('avg_age', 0):.2f} anos")
            
            with col2:
                st.metric("HbA1c Média", f"{stats.get('avg_hba1c', 0):.2f}%")
            
            with col3:
                st.metric("BMI Média", f"{stats.get('avg_bmi', 0):.2f}")
        
        # Dados processados
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
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.info("Execute o notebook 04_export_to_dashboard.ipynb para exportar os dados.")

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

# Página 3: Performance dos Modelos
elif page == "🤖 Performance dos Modelos":
    st.header("Performance dos Modelos de Machine Learning")
    
    try:
        # Buscar métricas do banco
        query = "SELECT * FROM model_metrics ORDER BY accuracy DESC"
        metrics_df = pd.read_sql(query, engine)
        
        if not metrics_df.empty:
            st.subheader("Comparação de Modelos")
            
            # Tabela de métricas
            display_df = metrics_df[['model_name', 'accuracy', 'f1_score_weighted', 'f1_score_macro']].copy()
            display_df.columns = ['Modelo', 'Accuracy', 'F1-Score (Weighted)', 'F1-Score (Macro)']
            display_df = display_df.round(4)
            st.dataframe(display_df, use_container_width=True)
            
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
            st.success(f"🏆 **Melhor Modelo**: {best_model['model_name']} com Accuracy de {best_model['accuracy']:.4f}")
            
            # Métricas detalhadas por modelo
            st.subheader("Métricas Detalhadas por Modelo")
            selected_model = st.selectbox("Selecione um modelo para ver detalhes:", metrics_df['model_name'].unique())
            
            model_metrics = metrics_df[metrics_df['model_name'] == selected_model].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Accuracy", f"{model_metrics['accuracy']:.4f}")
            
            with col2:
                st.metric("F1-Score (weighted)", f"{model_metrics['f1_score_weighted']:.4f}")
            
            with col3:
                st.metric("F1-Score (macro)", f"{model_metrics['f1_score_macro']:.4f}")
            
            with col4:
                st.metric("Precision (Y)", f"{model_metrics.get('precision_y', 0):.4f}")
            
            # Métricas por classe
            metrics_by_class = pd.DataFrame({
                'Classe': ['N (Não Diabético)', 'P (Pré-Diabético)', 'Y (Diabético)'],
                'Precision': [
                    model_metrics.get('precision_n', 0),
                    model_metrics.get('precision_p', 0),
                    model_metrics.get('precision_y', 0)
                ],
                'Recall': [
                    model_metrics.get('recall_n', 0),
                    model_metrics.get('recall_p', 0),
                    model_metrics.get('recall_y', 0)
                ]
            })
            
            fig2 = go.Figure()
            
            fig2.add_trace(go.Bar(
                name='Precision',
                x=metrics_by_class['Classe'],
                y=metrics_by_class['Precision'],
                marker_color='#3498db'
            ))
            
            fig2.add_trace(go.Bar(
                name='Recall',
                x=metrics_by_class['Classe'],
                y=metrics_by_class['Recall'],
                marker_color='#2ecc71'
            ))
            
            fig2.update_layout(
                title=f"Métricas por Classe - {selected_model}",
                xaxis_title="Classe",
                yaxis_title="Score",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Nenhuma métrica de modelo encontrada. Execute o notebook 02_preprocessing_and_modeling.ipynb primeiro.")
        
        # Informações do MLFlow
        st.subheader("Experimentos no MLFlow")
        if mlflow_client:
            try:
                experiments = mlflow_client.search_experiments()
                if experiments:
                    for exp in experiments[:5]:
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

# Página 4: Predições em Tempo Real
elif page == "⚡ Predições em Tempo Real":
    st.header("Predições e Resultados em Tempo Real")
    
    try:
        # Predições recentes
        st.subheader("Predições Recentes dos Modelos")
        
        pred_query = "SELECT * FROM model_predictions ORDER BY created_at DESC LIMIT 50"
        predictions_df = pd.read_sql(pred_query, engine)
        
        if not predictions_df.empty:
            st.dataframe(predictions_df, use_container_width=True)
            
            # Gráfico de predições ao longo do tempo
            if 'created_at' in predictions_df.columns:
                predictions_df['created_at'] = pd.to_datetime(predictions_df['created_at'])
                pred_counts = predictions_df.groupby([predictions_df['created_at'].dt.date, 'predicted_class']).size().reset_index(name='count')
                
                fig = px.bar(
                    pred_counts,
                    x='created_at',
                    y='count',
                    color='predicted_class',
                    title="Predições por Data e Classe",
                    labels={'created_at': 'Data', 'count': 'Número de Predições', 'predicted_class': 'Classe'},
                    color_discrete_map={'N': '#2ecc71', 'P': '#f39c12', 'Y': '#e74c3c'}
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma predição encontrada. Execute os notebooks de modelagem para gerar predições.")
        
        # Estatísticas atualizadas
        st.subheader("Estatísticas Atualizadas do Dataset")
        try:
            stats_query = "SELECT * FROM dataset_stats LIMIT 1"
            stats_df = pd.read_sql(stats_query, engine)
            
            if not stats_df.empty:
                stats = stats_df.iloc[0]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Idade Média", f"{stats.get('avg_age', 0):.2f} anos")
                
                with col2:
                    st.metric("HbA1c Média", f"{stats.get('avg_hba1c', 0):.2f}%")
                
                with col3:
                    st.metric("BMI Média", f"{stats.get('avg_bmi', 0):.2f}")
        except:
            st.info("Execute o notebook 04_export_to_dashboard.ipynb para atualizar as estatísticas.")
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Trendz Analytics - Projeto AV2 Machine Learning | CESAR School 2025.2**")
st.markdown("Dashboard de visualização conforme especificação do projeto")
st.markdown("Made with Streamlit")

