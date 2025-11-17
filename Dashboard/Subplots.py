# FILE: pages/8_📈_Subplots.py
"""
Tela 8 — Subplots (plotly)
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title='Subplots', layout='wide')
st.title('📈 Subplots')

# Verifica se os dados estão carregados no session state
if 'df' not in st.session_state or st.session_state.df is None:
    st.error("📊 **Nenhum dataset carregado!**")
    st.info("Por favor, volte à página inicial e carregue um arquivo.")
    st.markdown("---")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("🏠 Voltar ao Menu Inicial", use_container_width=False):
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Carrega os dados do session state
df = st.session_state.df

# Processamento dos dados
df.columns = df.columns.str.strip()
num_cols = df.select_dtypes(include=['number']).columns.tolist()

if len(num_cols) >= 2:
    # Configurações dos subplots
    st.subheader("🔧 Configurações dos Subplots")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        coluna1 = st.selectbox("📊 Primeira coluna:", num_cols, index=0, key="col1")
    with col2:
        coluna2 = st.selectbox("📈 Segunda coluna:", num_cols, index=1 if len(num_cols) > 1 else 0, key="col2")
    with col3:
        tipo_grafico = st.selectbox("🎯 Tipo de gráfico:", ["Histograma", "Box Plot", "Violin"], key="tipo")
    
    # Criar subplots
    fig = make_subplots(
        rows=1, 
        cols=2, 
        subplot_titles=(
            f'{tipo_grafico} - {coluna1}', 
            f'{tipo_grafico} - {coluna2}'
        ),
        horizontal_spacing=0.15
    )
    
    # Adicionar traces baseado no tipo selecionado
    if tipo_grafico == "Histograma":
        fig.add_trace(go.Histogram(x=df[coluna1], name=coluna1, nbinsx=20), row=1, col=1)
        fig.add_trace(go.Histogram(x=df[coluna2], name=coluna2, nbinsx=20), row=1, col=2)
    elif tipo_grafico == "Box Plot":
        fig.add_trace(go.Box(y=df[coluna1], name=coluna1), row=1, col=1)
        fig.add_trace(go.Box(y=df[coluna2], name=coluna2), row=1, col=2)
    else:  # Violin
        fig.add_trace(go.Violin(y=df[coluna1], name=coluna1), row=1, col=1)
        fig.add_trace(go.Violin(y=df[coluna2], name=coluna2), row=1, col=2)
    
    # Atualizar layout
    fig.update_layout(
        template='plotly_dark',
        height=500,
        showlegend=False,
        title_text=f"Comparação: {coluna1} vs {coluna2}",
        title_x=0.5
    )
    
    # Melhorar formatação dos eixos
    fig.update_xaxes(title_text=coluna1, row=1, col=1)
    fig.update_xaxes(title_text=coluna2, row=1, col=2)
    fig.update_yaxes(title_text="Valores" if tipo_grafico != "Histograma" else "Frequência", row=1, col=1)
    fig.update_yaxes(title_text="Valores" if tipo_grafico != "Histograma" else "Frequência", row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Estatísticas descritivas
    st.subheader("📋 Estatísticas Descritivas")
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        st.write(f"**📊 {coluna1}**")
        st.dataframe(
            df[coluna1].describe().round(2),
            use_container_width=True,
            height=300
        )
    
    with stats_col2:
        st.write(f"**📈 {coluna2}**")
        st.dataframe(
            df[coluna2].describe().round(2),
            use_container_width=True,
            height=300
        )
    
    # Informações adicionais
    with st.expander("💡 Análise Comparativa"):
        correlacao = df[[coluna1, coluna2]].corr().iloc[0,1]
        st.write(f"**Correlação entre {coluna1} e {coluna2}:** {correlacao:.3f}")
        
        if correlacao > 0.7:
            st.success("✅ Forte correlação positiva")
        elif correlacao < -0.7:
            st.success("✅ Forte correlação negativa")
        elif abs(correlacao) < 0.3:
            st.info("🔍 Correlação fraca")
        else:
            st.info("📝 Correlação moderada")

elif len(num_cols) == 1:
    st.warning('⚠️ Apenas uma coluna numérica encontrada no dataset.')
    st.info(f'Coluna numérica disponível: **{num_cols[0]}**')
    
    # Plot único como fallback
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df[num_cols[0]], nbinsx=20))
    fig.update_layout(
        title=f'Histograma - {num_cols[0]}',
        template='plotly_dark',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.error('❌ Nenhuma coluna numérica encontrada no dataset.')
    st.info("Verifique se o dataset contém colunas com valores numéricos.")

st.markdown("---")
st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
if st.button("🏠 Voltar ao Menu Inicial", use_container_width=False):
    st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)