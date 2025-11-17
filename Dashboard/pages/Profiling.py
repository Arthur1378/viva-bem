# FILE: pages/5_📋_Profiling_de_Dados.py
"""
Tela 5 — Profiling (simplificado)
"""
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Profiling', layout='wide')
st.title('📋 Profiling de Dados')

# Verifica se os dados estão carregados
if 'df' not in st.session_state:
    st.error("⚠️ Nenhum dataset carregado. Por favor, volte à página inicial e carregue os dados.")
    st.stop()

# Carrega os dados do session state
df = st.session_state.df

# Sidebar com controles
with st.sidebar:
    st.header("⚙️ Configurações do Profiling")
    
    max_colunas = st.slider(
        "Máximo de colunas para mostrar", 
        min_value=1, 
        max_value=20, 
        value=8,
        help="Número máximo de gráficos a serem exibidos"
    )
    
    mostrar_nulos = st.checkbox("Mostrar informações de valores nulos", True)
    mostrar_estatisticas = st.checkbox("Mostrar estatísticas detalhadas", True)
    
    # Filtro por tipo de coluna
    tipo_dados = st.multiselect(
        "Tipos de dados para análise:",
        ["numéricas", "categóricas", "datas"],
        default=["numéricas"]
    )

# Estatísticas gerais do dataset
st.subheader("📊 Visão Geral do Dataset")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Linhas", f"{df.shape[0]:,}")
with col2:
    st.metric("Total de Colunas", df.shape[1])
with col3:
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    st.metric("Colunas Numéricas", len(num_cols))
with col4:
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    st.metric("Colunas Categóricas", len(cat_cols))

# Informações de qualidade dos dados
if mostrar_nulos:
    nulos_total = df.isnull().sum().sum()
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Valores Nulos Totais", nulos_total)
    
    with col2:
        percentual_nulos = (nulos_total / (df.shape[0] * df.shape[1])) * 100
        st.metric("Percentual de Nulos", f"{percentual_nulos:.2f}%")
    
    # Detalhes dos nulos por coluna
    if nulos_total > 0:
        with st.expander("🔍 Detalhes dos Valores Nulos por Coluna"):
            nulos_por_coluna = df.isnull().sum()
            colunas_com_nulos = nulos_por_coluna[nulos_por_coluna > 0].sort_values(ascending=False)
            
            for coluna, nulos in colunas_com_nulos.items():
                percentual = (nulos / len(df)) * 100
                st.write(f"**{coluna}**: {nulos} nulos ({percentual:.1f}%)")
                st.progress(percentual / 100)

# Análise de colunas numéricas
if "numéricas" in tipo_dados and num_cols:
    st.subheader("📈 Análise de Colunas Numéricas")
    
    # Seleção de colunas para análise
    colunas_selecionadas = st.multiselect(
        "Selecione as colunas numéricas para análise:",
        num_cols,
        default=num_cols[:min(4, len(num_cols))],
        key="num_cols_select"
    )
    
    if colunas_selecionadas:
        colunas_para_mostrar = colunas_selecionadas[:max_colunas]
        
        for i, coluna in enumerate(colunas_para_mostrar):
            with st.expander(f"📊 **{coluna}** - Análise Detalhada", expanded=True):
                
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    # Gráfico de distribuição
                    fig = px.histogram(
                        df, 
                        x=coluna,
                        nbins=30,
                        title=f'Distribuição de {coluna}',
                        template='plotly_dark',
                        color_discrete_sequence=['#00FF88']
                    )
                    fig.update_layout(
                        showlegend=False,
                        height=400,
                        xaxis_title=coluna,
                        yaxis_title="Frequência"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_right:
                    if mostrar_estatisticas:
                        st.write("**📋 Estatísticas Descritivas:**")
                        
                        stats = df[coluna].describe()
                        nulos = df[coluna].isnull().sum()
                        
                        st.metric("Média", f"{stats['mean']:.2f}")
                        st.metric("Mediana", f"{df[coluna].median():.2f}")
                        st.metric("Desvio Padrão", f"{stats['std']:.2f}")
                        st.metric("Mínimo", f"{stats['min']:.2f}")
                        st.metric("Máximo", f"{stats['max']:.2f}")
                        st.metric("Valores Nulos", nulos)
                        
                        # Skewness
                        skewness = df[coluna].skew()
                        st.metric("Assimetria (Skewness)", f"{skewness:.2f}")
                        
                        # Interpretação do skewness
                        if abs(skewness) > 1:
                            skew_text = "Fortemente assimétrica"
                        elif abs(skewness) > 0.5:
                            skew_text = "Moderadamente assimétrica"
                        else:
                            skew_text = "Aproximadamente simétrica"
                        
                        st.write(f"*Distribuição: {skew_text}*")

                # Barra de progresso
                if len(colunas_para_mostrar) > 1:
                    st.progress(
                        (i + 1) / len(colunas_para_mostrar), 
                        text=f"Processando {i + 1} de {len(colunas_para_mostrar)} colunas"
                    )

# Análise de colunas categóricas
if "categóricas" in tipo_dados and cat_cols:
    st.subheader("📊 Análise de Colunas Categóricas")
    
    colunas_cat_selecionadas = st.multiselect(
        "Selecione as colunas categóricas para análise:",
        cat_cols,
        default=cat_cols[:min(3, len(cat_cols))],
        key="cat_cols_select"
    )
    
    for coluna in colunas_cat_selecionadas[:max_colunas]:
        with st.expander(f"📋 **{coluna}** - Análise Categórica"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gráfico de barras para categorias
                contagem = df[coluna].value_counts().head(15)  # Top 15 categorias
                fig = px.bar(
                    x=contagem.index,
                    y=contagem.values,
                    title=f'Top Categorias - {coluna}',
                    template='plotly_dark',
                    color_discrete_sequence=['#FFAA00']
                )
                fig.update_layout(
                    xaxis_title=coluna,
                    yaxis_title="Contagem",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Estatísticas:**")
                unique_count = df[coluna].nunique()
                nulos = df[coluna].isnull().sum()
                moda = df[coluna].mode()
                moda_val = moda[0] if not moda.empty else "N/A"
                
                st.metric("Valores Únicos", unique_count)
                st.metric("Valores Nulos", nulos)
                st.metric("Moda", str(moda_val)[:20] + "..." if len(str(moda_val)) > 20 else str(moda_val))

# Resumo final
st.markdown("---")
st.subheader("📋 Resumo do Profiling")

col1, col2 = st.columns(2)

with col1:
    st.write("**✅ Pontos Fortes:**")
    if nulos_total == 0:
        st.write("• Sem valores nulos")
    if len(num_cols) > 0:
        st.write(f"• {len(num_cols)} colunas numéricas para análise")
    if len(cat_cols) > 0:
        st.write(f"• {len(cat_cols)} colunas categóricas para análise")

with col2:
    st.write("**⚠️ Atenção:**")
    if nulos_total > 0:
        st.write("• Valores nulos presentes")
    if len(df) < 100:
        st.write("• Dataset pequeno (pode afetar análises)")
    colunas_com_muitos_nulos = [col for col in df.columns if df[col].isnull().sum() / len(df) > 0.5]
    if colunas_com_muitos_nulos:
        st.write(f"• {len(colunas_com_muitos_nulos)} coluna(s) com >50% de nulos")

# Navegação
st.markdown("---")
st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
if st.button("🏠 Voltar ao Menu Inicial", use_container_width=False):
    st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)