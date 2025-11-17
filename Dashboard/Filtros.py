# FILE: pages/2_🔍_Filtrando_um_DataFrame.py
"""
Tela 2 — Filtragem Interativa de Dados (Versão com Session State)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ---------------------------------------------------------------------
# ⚙️ CONFIGURAÇÕES INICIAIS
# ---------------------------------------------------------------------
st.set_page_config(page_title='Filtragem', layout='wide')
st.title('🔍 Filtros do DataFrame')

# ---------------------------------------------------------------------
# 📂 VERIFICAÇÃO E CARREGAMENTO DOS DADOS
# ---------------------------------------------------------------------
if 'df' not in st.session_state:
    st.error("⚠️ Nenhum dataset carregado. Por favor, volte ao Menu Inicial e carregue seus dados.")
    st.page_link("app.py", label="🏠 Voltar ao Menu Inicial")
    st.stop()

# Carrega os dados do session state
df = st.session_state.df

# Validação do DataFrame
if df.empty:
    st.warning("📭 O dataset carregado está vazio.")
    st.stop()

# ---------------------------------------------------------------------
# 📌 DETECÇÃO AUTOMÁTICA DE COLUNAS
# ---------------------------------------------------------------------
text_cols = df.select_dtypes(include=['object']).columns.tolist()
num_cols = df.select_dtypes(include=['number']).columns.tolist()

# Heurística para coluna de descrição
possible_names = [
    c for c in text_cols
    if any(k in c.lower() for k in ['alimento', 'nome', 'produto', 'categoria', 'descr', 'item', 'food'])
]
auto_desc_col = possible_names[0] if possible_names else None

# ---------------------------------------------------------------------
# 🎛️ SEÇÃO DE FILTROS
# ---------------------------------------------------------------------
st.subheader('🎛️ Filtros Interativos')

col_f1, col_f2 = st.columns(2)

# Seleção da coluna de descrição
with col_f1:
    desc_col = st.selectbox(
        "**Coluna de descrição:**",
        options=["(Nenhuma)"] + text_cols,
        index=(text_cols.index(auto_desc_col) + 1) if auto_desc_col else 0,
        help="Selecione a coluna que contém os nomes dos alimentos/produtos"
    )

# Filtro por nome
with col_f2:
    if desc_col != "(Nenhuma)":
        valores = sorted(df[desc_col].dropna().unique().tolist())
        
        # 🔄 MULTIPLAS SELEÇÕES (NOVA FUNCIONALIDADE)
        nomes_selecionados = st.multiselect(
            "**Filtrar por itens específicos:**",
            options=valores,
            default=valores[:1] if valores else [],
            help="Selecione um ou mais itens para filtrar"
        )
        
        # Indicador de dados ausentes
        if df[desc_col].isna().any():
            st.caption(f"⚠️ {df[desc_col].isna().sum()} valores ausentes nesta coluna")
    else:
        nomes_selecionados = []

st.markdown("---")

# ---------------------------------------------------------------------
# 📊 FILTROS NUMÉRICOS COM SLIDERS
# ---------------------------------------------------------------------
st.subheader("📊 Filtros por Faixa Numérica")

if not num_cols:
    st.info("ℹ️ Nenhuma coluna numérica encontrada para filtros.")
else:
    ranges = {}
    cols = st.columns(2)
    
    for i, c in enumerate(num_cols):
        col_idx = i % 2
        with cols[col_idx]:
            if pd.notna(df[c].min()) and pd.notna(df[c].max()) and df[c].min() < df[c].max():
                mi, ma = df[c].min(), df[c].max()
                ranges[c] = st.slider(
                    label=f"**{c}:**",
                    min_value=float(mi),
                    max_value=float(ma),
                    value=(float(mi), float(ma)),
                    help=f"Faixa: {mi:.2f} a {ma:.2f}"
                )

# ---------------------------------------------------------------------
# 🔄 BOTÃO DE RESET (NOVA FUNCIONALIDADE)
# ---------------------------------------------------------------------
col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
with col_reset2:
    if st.button("🔄 Resetar Todos os Filtros", type="secondary", use_container_width=True):
        # Limpa apenas os filtros, mantendo os dados
        st.rerun()

# ---------------------------------------------------------------------
# 🧮 APLICAÇÃO DOS FILTROS (OTIMIZADA)
# ---------------------------------------------------------------------
# Aplicação eficiente usando máscaras booleanas
mask = pd.Series(True, index=df.index)

# Filtro por descrição
if desc_col != "(Nenhuma)" and nomes_selecionados:
    mask &= df[desc_col].isin(nomes_selecionados)

# Filtros numéricos
for c, (low, high) in ranges.items():
    mask &= (df[c] >= low) & (df[c] <= high)

filtered = df[mask]

# ---------------------------------------------------------------------
# 📈 PAINEL DE MÉTRICAS (NOVA FUNCIONALIDADE)
# ---------------------------------------------------------------------
st.subheader("📊 Painel de Resultados")

if filtered.empty:
    st.warning('❌ Nenhum registro encontrado com os filtros aplicados.')
else:
    # Métricas do filtro
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Registros Encontrados", len(filtered))
    with col2:
        st.metric("Total de Registros", len(df))
    with col3:
        percentual = (len(filtered) / len(df)) * 100
        st.metric("Percentual", f"{percentual:.1f}%")
    with col4:
        st.metric("Colunas", len(df.columns))

# ---------------------------------------------------------------------
# 📥 EXPORTAÇÃO DE DADOS (NOVA FUNCIONALIDADE)
# ---------------------------------------------------------------------
if not filtered.empty:
    st.subheader("💾 Exportação de Dados")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # Exportar CSV
        csv = filtered.to_csv(index=False)
        st.download_button(
            label="📥 Exportar como CSV",
            data=csv,
            file_name="dados_filtrados.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_exp2:
        # Exportar Excel
        @st.cache_data
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Dados_Filtrados')
            return output.getvalue()
        
        excel_data = to_excel(filtered)
        st.download_button(
            label="📊 Exportar como Excel",
            data=excel_data,
            file_name="dados_filtrados.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )

# ---------------------------------------------------------------------
# 📊 SEÇÃO DE GRÁFICOS
# ---------------------------------------------------------------------
st.subheader('📈 Visualizações Gráficas')

if not filtered.empty:
    # Seleção de colunas para histogramas
    show_cols = st.multiselect(
        "**Selecione as colunas para visualização:**",
        options=num_cols,
        default=num_cols[:min(3, len(num_cols))],
        help="Escolha as colunas numéricas para gerar histogramas"
    )
    
    if show_cols:
        # Layout responsivo para gráficos
        cols_per_row = 2
        for i, coluna in enumerate(show_cols):
            if i % cols_per_row == 0:
                chart_cols = st.columns(cols_per_row)
            
            with chart_cols[i % cols_per_row]:
                fig = px.histogram(
                    filtered,
                    x=coluna,
                    nbins=20,
                    template='plotly_white',
                    title=f'Distribuição de {coluna}',
                    color_discrete_sequence=['#1f77b4']
                )
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # 🔄 GRÁFICO DE CORRELAÇÃO (NOVA FUNCIONALIDADE)
    if len(num_cols) >= 2:
        st.subheader("📈 Matriz de Correlação")
        
        col_corr1, col_corr2 = st.columns([3, 1])
        
        with col_corr1:
            # Calcular matriz de correlação
            corr_matrix = filtered[num_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title='Matriz de Correlação entre Variáveis Numéricas'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_corr2:
            st.info("""
            **💡 Dica:**
            - Valores próximos de +1: correlação positiva forte
            - Valores próximos de -1: correlação negativa forte  
            - Valores próximos de 0: pouca ou nenhuma correlação
            """)

# ---------------------------------------------------------------------
# 🔙 VOLTAR AO MENU
# ---------------------------------------------------------------------
st.markdown("---")
st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
st.page_link("app.py", label="🏠 Voltar ao Menu Inicial", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 📝 INSTRUÇÕES DE USO (NOVA FUNCIONALIDADE)
# ---------------------------------------------------------------------
with st.expander("ℹ️ **Instruções de Uso**"):
    st.markdown("""
    **Como usar esta página:**
    
    1. **🎛️ Filtros Interativos** - Selecione colunas textuais e numéricas para filtrar
    2. **📊 Filtros Numéricos** - Use os sliders para definir faixas de valores
    3. **📈 Visualizações** - Veja histogramas e correlações dos dados filtrados
    4. **💾 Exportação** - Baixe os resultados em CSV ou Excel
    5. **🔄 Reset** - Use o botão para limpar todos os filtros
    
    **Dica:** Os dados são mantidos na sessão, podendo ser compartilhados entre páginas.
    """)