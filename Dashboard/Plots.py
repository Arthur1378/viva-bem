# FILE: pages/7_📊_Plots.py
"""
Tela 7 — Plots variados
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title='Plots', layout='wide')
st.title('📊 Análise Visual dos Dados')

# Carrega os dados do session state
if 'df' not in st.session_state:
    st.error("⚠️ Nenhum dataset carregado. Por favor, volte à página inicial e carregue os dados.")
    st.stop()

df = st.session_state.df

# CORREÇÃO ROBUSTA: Remove colunas duplicadas definitivamente
def remove_duplicate_columns(df):
    """Remove colunas duplicadas de forma definitiva"""
    original_cols = df.columns.tolist()
    
    # Identifica colunas duplicadas
    duplicated_mask = df.columns.duplicated()
    duplicated_cols = df.columns[duplicated_mask].tolist()
    
    if duplicated_cols:
        st.warning(f"⚠️ Removendo colunas duplicadas: {list(set(duplicated_cols))}")
        
        # Remove colunas duplicadas, mantendo apenas a primeira ocorrência
        df_clean = df.loc[:, ~duplicated_mask]
        
        # Verifica se a limpeza foi bem sucedida
        cleaned_cols = df_clean.columns.tolist()
        st.info(f"✅ Colunas após limpeza: {len(cleaned_cols)} (antes: {len(original_cols)})")
        
        return df_clean
    return df

# Aplica a limpeza
df = remove_duplicate_columns(df)

# Preprocessamento básico
df.columns = df.columns.str.strip()
num_cols = df.select_dtypes(include=['number']).columns.tolist()
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# CORREÇÃO: Função alternativa segura para scatter plot
def create_scatter_safe(df, x_col, y_col, color_col=None, show_trend=False):
    """Cria scatter plot de forma segura, evitando problemas de colunas duplicadas"""
    try:
        # Cria um DataFrame limpo apenas com as colunas necessárias
        columns_needed = [x_col, y_col]
        if color_col and color_col in df.columns and color_col not in columns_needed:
            columns_needed.append(color_col)
        
        # Garante colunas únicas
        plot_df = df[columns_needed].copy()
        
        # Remove duplicatas por segurança
        plot_df = plot_df.loc[:, ~plot_df.columns.duplicated()]
        
        # Remove valores nulos
        plot_df = plot_df.dropna()
        
        if len(plot_df) == 0:
            st.warning("Não há dados suficientes após remover valores nulos")
            return None
        
        # Cria o gráfico
        if color_col and color_col in plot_df.columns:
            fig = px.scatter(plot_df, x=x_col, y=y_col, color=color_col,
                           template="plotly_white", 
                           title=f"Relação entre {x_col} e {y_col}")
        else:
            fig = px.scatter(plot_df, x=x_col, y=y_col,
                           template="plotly_white", 
                           title=f"Relação entre {x_col} e {y_col}")
        
        # Adiciona linha de tendência se solicitado
        if show_trend:
            try:
                # Adiciona linha de tendência manualmente para evitar conflitos
                from scipy import stats
                import numpy as np
                
                x_data = plot_df[x_col].dropna()
                y_data = plot_df[y_col].dropna()
                
                if len(x_data) > 1 and len(y_data) > 1:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
                    line_x = np.linspace(x_data.min(), x_data.max(), 100)
                    line_y = slope * line_x + intercept
                    
                    fig.add_trace(go.Scatter(
                        x=line_x, y=line_y,
                        mode='lines',
                        name=f'Tendência (R²={r_value**2:.3f})',
                        line=dict(color='red', dash='dash')
                    ))
            except Exception as e:
                st.warning("Não foi possível calcular a linha de tendência")
        
        return fig
        
    except Exception as e:
        st.error(f"Erro ao criar scatter plot: {str(e)}")
        return None

# CORREÇÃO: Função segura para boxplot
def create_boxplot_safe(df, columns):
    """Cria boxplot de forma segura"""
    try:
        # Cria DataFrame apenas com as colunas selecionadas
        plot_df = df[columns].copy()
        plot_df = plot_df.loc[:, ~plot_df.columns.duplicated()]
        
        fig = px.box(plot_df, y=columns, template="plotly_white",
                   title="Distribuição - Boxplots")
        return fig
    except Exception as e:
        st.error(f"Erro ao criar boxplot: {str(e)}")
        return None

# CORREÇÃO: Função segura para gráfico de barras
def create_bar_chart_safe(df, group_by, agg_method, agg_cols=None):
    """Cria gráfico de barras de forma segura"""
    try:
        if agg_method == "Contagem":
            df_agg = df.groupby(group_by).size().reset_index(name='Contagem')
            fig_bar = px.bar(df_agg, x=group_by, y='Contagem',
                           title=f'Contagem de Registros por {group_by}',
                           template="plotly_white")
            return fig_bar
        else:
            if agg_cols:
                # Mapeia método de agregação
                agg_map = {
                    "Soma": "sum",
                    "Média": "mean", 
                    "Mediana": "median",
                    "Máximo": "max",
                    "Mínimo": "min"
                }
                
                # Cria DataFrame seguro para agregação
                plot_df = df[[group_by] + agg_cols].copy()
                plot_df = plot_df.loc[:, ~plot_df.columns.duplicated()]
                
                df_agg = plot_df.groupby(group_by)[agg_cols].agg(agg_map[agg_method]).reset_index()
                
                # Gráfico de barras agrupado
                fig_bar = px.bar(df_agg, x=group_by, y=agg_cols,
                               title=f'{agg_method} por {group_by}',
                               template="plotly_white",
                               barmode='group')
                return fig_bar
            else:
                st.info("Selecione colunas para agregar")
                return None
    except Exception as e:
        st.error(f"Erro ao criar gráfico de barras: {str(e)}")
        return None

# Cria abas para diferentes tipos de visualização
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Boxplots & Histogramas", 
    "🔍 Dispersão & Correlação", 
    "📊 Barras & Agregações", 
    "📋 Estatísticas"
])

with tab1:
    st.header("Análise de Distribuição")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Boxplots")
        if num_cols:
            box_cols = st.multiselect(
                "Selecione colunas para boxplot:",
                num_cols,
                default=num_cols[:3] if len(num_cols) >= 3 else num_cols,
                key="boxplot_cols"
            )
            if box_cols:
                fig_box = create_boxplot_safe(df, box_cols)
                if fig_box:
                    st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Selecione colunas para visualizar os boxplots")
        else:
            st.warning("Não há colunas numéricas para boxplots")
    
    with col2:
        st.subheader("Histogramas")
        if num_cols:
            hist_col = st.selectbox(
                "Selecione coluna para histograma:",
                num_cols,
                key="hist_col"
            )
            if hist_col:
                try:
                    # Cria DataFrame seguro para histograma
                    plot_data = df[[hist_col]].copy()
                    plot_data = plot_data.loc[:, ~plot_data.columns.duplicated()]
                    
                    fig_hist = px.histogram(plot_data, x=hist_col, template="plotly_white",
                                          title=f"Distribuição de {hist_col}",
                                          nbins=st.slider("Número de bins:", 5, 100, 30, key="hist_bins"))
                    st.plotly_chart(fig_hist, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao criar histograma: {str(e)}")
        else:
            st.warning("Não há colunas numéricas para histogramas")

with tab2:
    st.header("Análise de Relacionamento")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configurações")
        if len(num_cols) >= 2:
            scatter_x = st.selectbox("Eixo X:", num_cols, key="scatter_x")
            scatter_y = st.selectbox("Eixo Y:", num_cols, key="scatter_y")
            scatter_color = st.selectbox("Colorir por:", [None] + cat_cols, key="scatter_color")
            
            show_trend = st.checkbox("Mostrar linha de tendência", value=True, key="show_trend")
            
        else:
            st.warning("São necessárias pelo menos 2 colunas numéricas para scatter plot")
    
    with col2:
        st.subheader("Gráfico de Dispersão")
        if len(num_cols) >= 2:
            # Usa função segura para scatter plot
            fig_scatter = create_scatter_safe(df, scatter_x, scatter_y, scatter_color, show_trend)
            if fig_scatter:
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Heatmap de correlação
            st.subheader("Matriz de Correlação")
            if len(num_cols) > 1:
                try:
                    # Cria DataFrame seguro para correlação
                    corr_df = df[num_cols].copy()
                    corr_df = corr_df.loc[:, ~corr_df.columns.duplicated()]
                    
                    corr_matrix = corr_df.corr()
                    fig_heatmap = px.imshow(corr_matrix, 
                                          color_continuous_scale='RdBu_r',
                                          title='Correlação entre Variáveis Numéricas',
                                          aspect="auto")
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao criar heatmap: {str(e)}")

with tab3:
    st.header("Análise de Agregações")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configurações")
        
        # Seleção de agrupamento
        group_by = st.selectbox("Agrupar por:", [None] + cat_cols, key="group_by")
        
        # Método de agregação
        agg_method = st.selectbox("Método de agregação:", 
                                ["Soma", "Média", "Mediana", "Contagem", "Máximo", "Mínimo"],
                                key="agg_method")
        
        # Colunas para agregar
        if agg_method != "Contagem":
            agg_cols = st.multiselect("Colunas para agregar:", num_cols, key="agg_cols")
        else:
            agg_cols = None
    
    with col2:
        st.subheader("Visualização")
        
        if group_by:
            fig_bar = create_bar_chart_safe(df, group_by, agg_method, agg_cols)
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Selecione uma coluna para agrupamento")

with tab4:
    st.header("Estatísticas Descritivas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Resumo Estatístico")
        if num_cols:
            # Cria DataFrame seguro para estatísticas
            stats_df = df[num_cols].copy()
            stats_df = stats_df.loc[:, ~stats_df.columns.duplicated()]
            st.dataframe(stats_df.describe(), use_container_width=True)
        else:
            st.warning("Não há colunas numéricas para análise estatística")
    
    with col2:
        st.subheader("Informações do Dataset")
        st.metric("Total de Linhas", df.shape[0])
        st.metric("Total de Colunas", len(df.columns))  # Usa len() para contar colunas únicas
        st.metric("Colunas Numéricas", len(num_cols))
        st.metric("Colunas Categóricas", len(cat_cols))
        
        # Verifica se ainda há duplicatas
        has_duplicates = len(df.columns) != len(set(df.columns))
        if has_duplicates:
            st.error("❌ Ainda existem colunas duplicadas!")
        else:
            st.success("✅ Todas as colunas são únicas")

# Navegação inferior
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🏠 Voltar ao Menu Inicial", use_container_width=True):
        st.switch_page("app.py")