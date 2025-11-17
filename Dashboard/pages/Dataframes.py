# FILE: pages/1_🤝_Join_de_Dataframes.py
"""
Tela 1 — Join de DataFrames (versão profissional somente com gráficos)
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# Configuração da página
# -----------------------------------------------------------------------------
st.set_page_config(page_title="DataFrames", layout="wide")
st.title("🤝 DataFrames")

# -----------------------------------------------------------------------------
# Verificação e carregamento dos dados do session state
# -----------------------------------------------------------------------------
if 'df' not in st.session_state:
    st.error("⚠️ Dados não encontrados no session state.")
    st.info("Por favor, volte ao menu inicial e carregue os dados primeiro.")
    if st.button("🏠 Voltar ao Menu Inicial"):
        st.switch_page("app.py")
    st.stop()

# Carrega os dados do session state
df = st.session_state.df

# -----------------------------------------------------------------------------
# Validação básica dos dados
# -----------------------------------------------------------------------------
if df.empty:
    st.error("❌ O DataFrame carregado está vazio.")
    st.stop()

# -----------------------------------------------------------------------------
# Métricas
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Linhas", df.shape[0])
with col2:
    st.metric("Colunas", df.shape[1])
with col3:
    st.metric("Dados Carregados", "✅" if not df.empty else "❌")

# -----------------------------------------------------------------------------
# Gráfico da quantidade de valores por coluna textual
# -----------------------------------------------------------------------------
st.write("### 📊 Distribuição das Categorias por Coluna")

text_cols = df.select_dtypes(include=["object"]).columns.tolist()

if text_cols:
    # Seletor interativo de coluna
    coluna_selecionada = st.selectbox(
        "Selecione a coluna para análise:",
        options=text_cols,
        help="Escolha uma coluna textual para visualizar sua distribuição"
    )
    
    contagem = df[coluna_selecionada].value_counts().reset_index()
    contagem.columns = [coluna_selecionada, "Quantidade"]

    fig = px.bar(
        contagem,
        x=coluna_selecionada,
        y="Quantidade",
        text="Quantidade",
        title=f"Distribuição da coluna '{coluna_selecionada}'",
        template="plotly_dark"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Estatísticas rápidas
    st.write(f"**Estatísticas da coluna '{coluna_selecionada}':**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Valores Únicos", df[coluna_selecionada].nunique())
    with col2:
        st.metric("Valores Faltantes", df[coluna_selecionada].isnull().sum())
    with col3:
        st.metric("Categoria Mais Frequente", df[coluna_selecionada].mode().iloc[0] if not df[coluna_selecionada].empty else "N/A")
else:
    st.info("ℹ️ Não há colunas textuais para analisar graficamente.")

# -----------------------------------------------------------------------------
# Detecção da coluna de descrição com fallback interativo
# -----------------------------------------------------------------------------
st.write("### 🔍 Configuração do Join")

PALAVRAS_CHAVE = ["alimento", "nome", "produto", "categoria", "descr", "item", "descrição", "description"]

possible_names = [c for c in text_cols if any(k in c.lower() for k in PALAVRAS_CHAVE)]

if possible_names:
    col_desc = st.selectbox(
        "Coluna de descrição detectada automaticamente:",
        options=possible_names,
        index=0
    )
    st.success(f"✅ Coluna de descrição selecionada: **{col_desc}**")
elif text_cols:
    col_desc = st.selectbox(
        "Selecione manualmente a coluna de descrição:",
        options=text_cols
    )
    st.warning(f"⚠️ Coluna selecionada manualmente: **{col_desc}**")
else:
    st.error("❌ Não há colunas textuais disponíveis para realizar o join.")
    st.stop()

# -----------------------------------------------------------------------------
# Construção da tabela de lookup e join
# -----------------------------------------------------------------------------
st.write("### 🔗 Join de Demonstração")

use_categoria = "Categoria" in df.columns and df["Categoria"].nunique() < len(df)

if use_categoria:
    chave_join = "Categoria"
    lookup = df[[chave_join]].drop_duplicates().reset_index(drop=True)
    st.info("🔍 Utilizando coluna 'Categoria' como chave do join")
else:
    chave_join = col_desc
    lookup = df[[chave_join]].drop_duplicates().reset_index(drop=True)
    st.info(f"🔍 Utilizando coluna '{col_desc}' como chave do join")

lookup["Codigo"] = lookup.index + 1
df_join = df.merge(lookup, on=chave_join, how="left")

# Salva o resultado no session state para uso em outras páginas
st.session_state.df_join = df_join
st.session_state.chave_join = chave_join

# -----------------------------------------------------------------------------
# Visualizações pós-join
# -----------------------------------------------------------------------------
st.write("### 📈 Resultados do Join")

# Gráfico da coluna adicionada após o join
contagem_codigos = df_join["Codigo"].value_counts().reset_index()
contagem_codigos.columns = ["Codigo", "Quantidade"]

fig_cod = px.bar(
    contagem_codigos,
    x="Codigo",
    y="Quantidade",
    text="Quantidade",
    title="Quantidade por Código (após join)",
    template="plotly_dark"
)
fig_cod.update_traces(textposition="outside")
st.plotly_chart(fig_cod, use_container_width=True)

# Gráfico principal — Distribuição por chave do join
counts = df_join[chave_join].value_counts().reset_index()
counts.columns = [chave_join, "Quantidade"]

fig = px.bar(
    counts,
    x=chave_join,
    y="Quantidade",
    text="Quantidade",
    title=f"Quantidade por {chave_join} (após join)",
    template="plotly_dark",
)
fig.update_traces(textposition="outside")
fig.update_layout(xaxis_title=chave_join, yaxis_title="Quantidade")
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# Resumo do join
# -----------------------------------------------------------------------------
st.write("### 📋 Resumo do Join Realizado")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Chave Utilizada", chave_join)
with col2:
    st.metric("Códigos Gerados", lookup["Codigo"].nunique())
with col3:
    st.metric("Join Realizado", "✅ Sucesso")

# -----------------------------------------------------------------------------
# Navegação
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("---")
if st.button("🏠 Voltar ao Menu Inicial"):
    st.switch_page("app.py")