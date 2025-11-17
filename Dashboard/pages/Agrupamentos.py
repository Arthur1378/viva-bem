# FILE: pages/3_🦞_Agrupando_DataFrames.py
"""
Tela 3 — Agrupamentos (groupby) com análises avançadas
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ==========================================================
# CONFIGURAÇÕES DA PÁGINA
# ==========================================================
st.set_page_config(page_title='Agrupando', layout='wide')
st.title('🦞 Agrupando DataFrames')

# ==========================================================
# CARREGAMENTO DOS DADOS DO SESSION STATE
# ==========================================================

# Verifica se os dados estão carregados no session state
if 'df' not in st.session_state or st.session_state.df.empty:
    st.error("❌ Dados não carregados. Por favor, volte à página principal para carregar o dataset.")
    
    st.markdown("---")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("🏠 Voltar à Página Principal", type="primary"):
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Carrega os dados do session state
df = st.session_state.df

# ==========================================================
# SIDEBAR GLOBAL
# ==========================================================
st.sidebar.markdown("## 📊 Navegação")
st.sidebar.markdown("---")
if st.sidebar.button("🏠 Menu Principal"):
    st.switch_page("app.py")

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informações do Dataset")
st.sidebar.write(f"**Linhas:** {df.shape[0]}")
st.sidebar.write(f"**Colunas:** {df.shape[1]}")
st.sidebar.write(f"**Grupos disponíveis:** {df.select_dtypes(include=['object']).shape[1]}")

# ==========================================================
# PREPARAÇÃO DOS DADOS
# ==========================================================
df.columns = df.columns.str.strip()
text_cols = df.select_dtypes(include=['object']).columns.tolist()
num_cols = df.select_dtypes(include=['number']).columns.tolist()

if not text_cols:
    st.error("❌ Nenhuma coluna de texto encontrada para agrupamento.")
    st.info("💡 Adicione colunas com texto para usar as funcionalidades de agrupamento.")
    
    st.markdown("---")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("🏠 Voltar à Página Principal"):
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if not num_cols:
    st.error("❌ Nenhuma coluna numérica encontrada para análise.")
    st.info("💡 É necessário pelo menos uma coluna numérica para as análises.")
    
    st.markdown("---")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("🏠 Voltar à Página Principal"):
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================================
# SELEÇÃO DE PARÂMETROS
# ==========================================================
st.markdown("## ⚙️ Configuração da Análise")

col1, col2 = st.columns(2)

with col1:
    group_col = st.selectbox(
        "Agrupar por:", 
        text_cols,
        help="Selecione a coluna categórica para agrupar os dados"
    )

with col2:
    agg_col = st.selectbox(
        "Coluna numérica para análise:", 
        num_cols,
        help="Selecione a coluna numérica para calcular as estatísticas"
    )

# Métricas rápidas
st.markdown("### 📈 Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Grupos Únicos", df[group_col].nunique())
col2.metric("Média Geral", f"{df[agg_col].mean():.2f}")
col3.metric("Total Geral", f"{df[agg_col].sum():.2f}")
col4.metric("Valor Máximo", f"{df[agg_col].max():.2f}")

st.markdown("---")

# ==========================================================
# TABS - ANÁLISES AVANÇADAS
# ==========================================================
tabs = st.tabs([
    "📊 Agrupamento Simples",
    "📈 Distribuição",
    "🏆 Top N / Bottom N",
    "📉 Proporções",
    "📊 Pareto 80/20",
    "📉 Correlação por Grupo",
    "⏳ Séries Temporais"
])

# ==========================================================
# 1 — Agrupamento simples
# ==========================================================
with tabs[0]:
    st.subheader("📊 Estatísticas do Agrupamento")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        funcs = ['mean', 'sum', 'median', 'min', 'max', 'std', 'count']
        func = st.selectbox("Função de agregação:", funcs, key="agg_func")
        
        # Mostrar estatísticas do grupo selecionado
        if group_col:
            st.metric("Grupos Únicos", df[group_col].nunique())

    with col2:
        if group_col and agg_col:
            grouped = df.groupby(group_col)[agg_col].agg(func).reset_index()
            grouped = grouped.sort_values(agg_col, ascending=False)
            
            fig = px.bar(
                grouped, 
                x=group_col, 
                y=agg_col,
                template="plotly_white",
                title=f"{func.upper()} de {agg_col} por {group_col}",
                color=agg_col,
                color_continuous_scale="viridis"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela com dados
            with st.expander("📋 Ver dados tabulares"):
                st.dataframe(grouped, use_container_width=True)

# ==========================================================
# 2 — Distribuição
# ==========================================================
with tabs[1]:
    st.subheader("📈 Distribuição por Grupo")
    
    tipo = st.radio(
        "Tipo de visualização:", 
        ["Histograma", "Boxplot", "Violino", "Densidade"], 
        horizontal=True,
        key="dist_type"
    )

    if tipo == "Histograma":
        fig = px.histogram(
            df, x=agg_col, color=group_col, 
            template="plotly_white",
            title=f"Distribuição de {agg_col} por {group_col}",
            nbins=30
        )
    elif tipo == "Boxplot":
        fig = px.box(
            df, x=group_col, y=agg_col, 
            template="plotly_white",
            title=f"Boxplot de {agg_col} por {group_col}"
        )
        fig.update_layout(xaxis_tickangle=-45)
    elif tipo == "Violino":
        fig = px.violin(
            df, x=group_col, y=agg_col, 
            box=True, points="all", 
            template="plotly_white",
            title=f"Distribuição Violino de {agg_col} por {group_col}"
        )
        fig.update_layout(xaxis_tickangle=-45)
    else:
        # Heatmap de densidade
        if len(df[group_col].unique()) > 20:
            st.warning("⚠️ Muitos grupos para heatmap. Mostrando apenas os 20 principais.")
            top_groups = df[group_col].value_counts().head(20).index
            df_filtered = df[df[group_col].isin(top_groups)]
        else:
            df_filtered = df
            
        fig = px.density_heatmap(
            df_filtered, x=group_col, y=agg_col, 
            template="plotly_white",
            title=f"Mapa de Densidade: {agg_col} por {group_col}"
        )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# 3 — Top N / Bottom N
# ==========================================================
with tabs[2]:
    st.subheader("🏆 Ranking — Top N / Bottom N")

    N = st.slider("Número de itens no ranking:", 1, 20, 5, key="top_n")

    gsum = df.groupby(group_col)[agg_col].sum().sort_values(ascending=False)

    top_n = gsum.head(N).reset_index()
    bottom_n = gsum.tail(N).reset_index()

    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            top_n, x=group_col, y=agg_col, 
            template="plotly_white", 
            title=f"Top {N} - Maiores Valores",
            color=agg_col,
            color_continuous_scale="greens"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(f"📋 Top {N} - Dados"):
            st.dataframe(top_n, use_container_width=True)
    
    with col2:
        fig = px.bar(
            bottom_n, x=group_col, y=agg_col, 
            template="plotly_white", 
            title=f"Bottom {N} - Menores Valores",
            color=agg_col,
            color_continuous_scale="reds"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(f"📋 Bottom {N} - Dados"):
            st.dataframe(bottom_n, use_container_width=True)

# ==========================================================
# 4 — Proporções
# ==========================================================
with tabs[3]:
    st.subheader("📉 Proporções e Composição")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de pizza
        freq = df[group_col].value_counts().reset_index()
        freq.columns = [group_col, "contagem"]
        freq["percentual"] = (freq["contagem"] / freq["contagem"].sum() * 100).round(2)

        fig = px.pie(
            freq, 
            names=group_col, 
            values="contagem", 
            template="plotly_white",
            title=f"Proporção de Itens por {group_col}",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Total de Grupos", len(freq))
        st.metric("Grupo Mais Frequente", freq.iloc[0][group_col])
        st.metric("Frequência Máxima", f"{freq.iloc[0]['contagem']}")
        
        with st.expander("📊 Estatísticas"):
            st.write(freq.describe())

# ==========================================================
# 5 — Pareto
# ==========================================================
with tabs[4]:
    st.subheader("📊 Curva de Pareto 80/20")

    gsum = df.groupby(group_col)[agg_col].sum().sort_values(ascending=False)
    cum = gsum.cumsum() / gsum.sum() * 100

    # Encontrar ponto de 80%
    ponto_80 = None
    for i, (grupo, valor) in enumerate(cum.items()):
        if valor >= 80 and ponto_80 is None:
            ponto_80 = i + 1  # +1 porque é base 1

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Barras
    fig.add_trace(
        go.Bar(x=gsum.index, y=gsum.values, name="Valor", marker_color='blue'),
        secondary_y=False,
    )
    
    # Linha cumulativa
    fig.add_trace(
        go.Scatter(x=cum.index, y=cum.values, name="% Cumulativo", 
                  mode="lines+markers", line=dict(color='red', width=3)),
        secondary_y=True,
    )

    # Linha de 80%
    if ponto_80 is not None:
        fig.add_hline(y=80, line_dash="dash", line_color="green", 
                     annotation_text="80%", secondary_y=True)

    fig.update_layout(
        template="plotly_white", 
        xaxis_tickangle=-45,
        title="Análise de Pareto - 80/20"
    )
    fig.update_yaxes(title_text="Valor", secondary_y=False)
    fig.update_yaxes(title_text="Percentual Cumulativo", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
    
    if ponto_80:
        st.info(f"💡 **Princípio de Pareto**: Os primeiros {ponto_80} grupos representam 80% do total")

# ==========================================================
# 6 — Correlação por Grupo
# ==========================================================
with tabs[5]:
    st.subheader("📉 Correlação por Grupo")

    if len(num_cols) < 2:
        st.warning("⚠️ Necessário pelo menos duas colunas numéricas para análise de correlação.")
    else:
        col2 = st.selectbox(
            "Segunda coluna numérica:", 
            [c for c in num_cols if c != agg_col],
            key="corr_col"
        )

        correlations = []
        for g in df[group_col].unique():
            sub = df[df[group_col] == g]
            if len(sub) > 1:
                corr_value = sub[agg_col].corr(sub[col2])
                correlations.append({
                    group_col: g,
                    "correlacao": corr_value if not pd.isna(corr_value) else 0
                })

        corr_df = pd.DataFrame(correlations)
        corr_df = corr_df.sort_values("correlacao", ascending=False)

        fig = px.bar(
            corr_df, 
            x=group_col, 
            y="correlacao", 
            template="plotly_white",
            title=f"Correlação entre {agg_col} e {col2} por {group_col}",
            color="correlacao",
            color_continuous_scale="rdylgn"
        )
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_yaxes(range=[-1, 1])
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 Tabela de Correlações"):
            st.dataframe(corr_df, use_container_width=True)

# ==========================================================
# 7 — Séries Temporais
# ==========================================================
with tabs[6]:
    st.subheader("⏳ Séries Temporais")

    date_cols = df.select_dtypes(include=["datetime"]).columns.tolist()

    if not date_cols:
        st.warning("⚠️ Nenhuma coluna de data/hora encontrada no dataset.")
        st.info("💡 Para usar esta funcionalidade, inclua colunas do tipo datetime no seu dataset.")
    else:
        col_date = st.selectbox("Coluna de data:", date_cols, key="date_col")
        
        # Agrupar por data e calcular estatísticas
        df[col_date] = pd.to_datetime(df[col_date])
        ts_data = df.groupby(df[col_date].dt.date)[agg_col].agg(['sum', 'mean', 'count']).reset_index()
        ts_data.columns = ['data', 'soma', 'media', 'contagem']
        
        # Selecionar tipo de agregação
        agg_type = st.radio("Métrica:", ["Soma", "Média", "Contagem"], horizontal=True, key="ts_agg")
        
        if agg_type == "Soma":
            y_col = 'soma'
            title = f"Soma de {agg_col} ao Longo do Tempo"
        elif agg_type == "Média":
            y_col = 'media'
            title = f"Média de {agg_col} ao Longo do Tempo"
        else:
            y_col = 'contagem'
            title = f"Contagem de Registros ao Longo do Tempo"

        fig = px.line(
            ts_data, 
            x='data', 
            y=y_col, 
            markers=True, 
            template="plotly_white",
            title=title
        )
        fig.update_traces(line=dict(width=3))
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 Dados da Série Temporal"):
            st.dataframe(ts_data, use_container_width=True)

# ==========================================================
# BOTÃO VOLTAR
# ==========================================================
st.markdown("---")
st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
if st.button("🏠 Voltar ao Menu Inicial", type="primary"):
    st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)