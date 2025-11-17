# FILE: pages/4_🚫_Desabilitando_Booleans.py
"""
Tela 4 — Booleans e filtros binários
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(page_title='Booleans', layout='wide')
st.title('🚫 Desabilitando Booleans')

# ========== CARREGAMENTO VIA SESSION STATE ==========
if "df" not in st.session_state:
    st.error("⚠️ Dados não carregados. Volte ao menu inicial para upload.")
    if st.button("🏠 Voltar ao Menu Inicial"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df

# ========== DETECÇÃO ROBUSTA DE COLUNAS BOOLEANAS ==========
def detect_boolean_columns(df):
    """
    Detecta colunas que representam valores booleanos
    Suporta: 0/1, True/False, Sim/Não, S/N, Y/N, etc.
    """
    bool_cols = []
    
    for col_name in df.columns:
        if df[col_name].dtype == 'bool':
            bool_cols.append(col_name)
            continue
            
        # Para colunas não-booleanas, verifica se contêm apenas 2 valores
        unique_vals = df[col_name].dropna().unique()
        
        if len(unique_vals) == 2:
            val_set = set(unique_vals)
            # Pares booleanos comuns
            boolean_pairs = [
                {0, 1}, {True, False}, 
                {'0', '1'}, {'S', 'N'}, {'s', 'n'},
                {'Sim', 'Não'}, {'sim', 'não'}, {'SIM', 'NÃO'},
                {'Y', 'N'}, {'y', 'n'}, {'Yes', 'No'}, {'yes', 'no'}
            ]
            
            if any(val_set == pair for pair in boolean_pairs):
                bool_cols.append(col_name)
    
    return bool_cols

bool_cols = detect_boolean_columns(df)

# ========== INTERFACE PRINCIPAL ==========
if bool_cols:
    st.success(f"✅ {len(bool_cols)} coluna(s) booleana(s) detectada(s)")
    
    # Seletor da coluna booleana
    coluna_selecionada = st.selectbox(
        "Selecione a coluna booleana:",
        bool_cols,
        help="Colunas com apenas dois valores (Sim/Não, 0/1, etc.)"
    )
    
    # Converter para booleano se necessário
    if df[coluna_selecionada].dtype != 'bool':
        mapping = {
            0: False, 1: True, '0': False, '1': True,
            'S': True, 'N': False, 's': True, 'n': False,
            'Sim': True, 'Não': False, 'sim': True, 'não': False,
            'Y': True, 'N': False, 'y': True, 'n': False,
            'Yes': True, 'No': False, 'yes': True, 'no': False,
            True: True, False: False
        }
        df[coluna_selecionada] = df[coluna_selecionada].map(mapping)
    
    # Seleção do valor booleano
    valor_filtro = st.radio(
        "Filtrar por:",
        [True, False],
        format_func=lambda x: "✅ Verdadeiro (Sim/1)" if x else "❌ Falso (Não/0)",
        horizontal=True
    )
    
    # Aplicar filtro
    filtered_df = df[df[coluna_selecionada] == valor_filtro]
    
    # Layout em colunas para métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Registros", len(df))
    
    with col2:
        st.metric(
            "Registros Filtrados", 
            len(filtered_df),
            f"{len(filtered_df) - len(df)}" if len(filtered_df) != len(df) else "0"
        )
    
    with col3:
        st.metric(
            "Percentual", 
            f"{len(filtered_df)/len(df)*100:.1f}%"
        )
    
    if not filtered_df.empty:
        # ========== GRÁFICOS VISUAIS ==========
        st.subheader("📊 Visualização Gráfica dos Dados Filtrados")
        
        # Layout com tabs para diferentes visualizações
        tab1, tab2, tab3 = st.tabs(["📈 Análise Numérica", "📊 Distribuição", "🔍 Comparação"])
        
        with tab1:
            # Gráfico de distribuição das colunas numéricas
            colunas_numericas = filtered_df.select_dtypes(include=['number']).columns
            
            if not colunas_numericas.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Box plot para análise de distribuição
                    coluna_box = st.selectbox(
                        "Selecione a coluna para box plot:",
                        colunas_numericas,
                        key="box_plot"
                    )
                    
                    fig_box = px.box(
                        filtered_df,
                        y=coluna_box,
                        title=f"Distribuição de {coluna_box}",
                        color_discrete_sequence=['#FF6B6B']
                    )
                    fig_box.update_layout(height=400)
                    st.plotly_chart(fig_box, use_container_width=True)
                
                with col2:
                    # Gráfico de violino para distribuição detalhada
                    coluna_violin = st.selectbox(
                        "Selecione a coluna para gráfico de violino:",
                        colunas_numericas,
                        key="violin_plot"
                    )
                    
                    fig_violin = px.violin(
                        filtered_df,
                        y=coluna_violin,
                        title=f"Distribuição Detalhada de {coluna_violin}",
                        box=True,
                        points="all",
                        color_discrete_sequence=['#4ECDC4']
                    )
                    fig_violin.update_layout(height=400)
                    st.plotly_chart(fig_violin, use_container_width=True)
            else:
                st.info("📈 Nenhuma coluna numérica disponível para análise.")
        
        with tab2:
            # Histogramas e distribuições
            colunas_numericas = filtered_df.select_dtypes(include=['number']).columns
            
            if not colunas_numericas.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Histograma interativo
                    coluna_hist = st.selectbox(
                        "Selecione a coluna para histograma:",
                        colunas_numericas,
                        key="histogram"
                    )
                    
                    fig_hist = px.histogram(
                        filtered_df,
                        x=coluna_hist,
                        title=f"Histograma de {coluna_hist}",
                        nbins=20,
                        color_discrete_sequence=['#45B7D1'],
                        opacity=0.8
                    )
                    fig_hist.update_layout(
                        height=400,
                        xaxis_title=coluna_hist,
                        yaxis_title="Frequência"
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Gráfico de densidade
                    coluna_density = st.selectbox(
                        "Selecione a coluna para densidade:",
                        colunas_numericas,
                        key="density"
                    )
                    
                    fig_density = px.histogram(
                        filtered_df,
                        x=coluna_density,
                        title=f"Distribuição de Densidade - {coluna_density}",
                        nbins=20,
                        color_discrete_sequence=['#96CEB4'],
                        opacity=0.7,
                        marginal="rug"
                    )
                    fig_density.update_layout(height=400)
                    st.plotly_chart(fig_density, use_container_width=True)
            else:
                st.info("📊 Nenhuma coluna numérica disponível para histogramas.")
        
        with tab3:
            # Comparação entre grupos booleanos
            st.subheader("🔍 Comparação entre Grupos Booleanos")
            
            # Gráfico de comparação dos dois grupos
            colunas_comparacao = df.select_dtypes(include=['number']).columns
            
            if not colunas_comparacao.empty:
                coluna_comp = st.selectbox(
                    "Selecione a coluna para comparação:",
                    colunas_comparacao,
                    key="comparison"
                )
                
                # Cria subplots para comparação
                fig_comp = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=[f'✅ {coluna_selecionada} = True', f'❌ {coluna_selecionada} = False'],
                    specs=[[{"type": "box"}, {"type": "box"}]]
                )
                
                # Dados para True
                dados_true = df[df[coluna_selecionada] == True][coluna_comp].dropna()
                # Dados para False
                dados_false = df[df[coluna_selecionada] == False][coluna_comp].dropna()
                
                fig_comp.add_trace(
                    go.Box(y=dados_true, name="Verdadeiro", marker_color='#2E8B57'),
                    row=1, col=1
                )
                
                fig_comp.add_trace(
                    go.Box(y=dados_false, name="Falso", marker_color='#DC143C'),
                    row=1, col=2
                )
                
                fig_comp.update_layout(
                    height=500,
                    title_text=f"Comparação de {coluna_comp} entre Grupos Booleanos",
                    showlegend=False
                )
                
                st.plotly_chart(fig_comp, use_container_width=True)
                
                # Estatísticas descritivas
                st.subheader("📋 Estatísticas Descritivas")
                col_stat1, col_stat2 = st.columns(2)
                
                with col_stat1:
                    st.write(f"**✅ {coluna_selecionada} = True**")
                    st.write(dados_true.describe())
                
                with col_stat2:
                    st.write(f"**❌ {coluna_selecionada} = False**")
                    st.write(dados_false.describe())
            else:
                st.info("🔍 Nenhuma coluna numérica disponível para comparação.")
    
    else:
        st.warning("⚠️ Nenhum registro corresponde ao filtro aplicado.")
        
        # Mostra gráfico da distribuição original da coluna booleana
        st.subheader("📊 Distribuição Original da Coluna Booleana")
        
        contagem_valores = df[coluna_selecionada].value_counts()
        fig_pie = px.pie(
            values=contagem_valores.values,
            names=contagem_valores.index.astype(str),
            title=f"Distribuição de {coluna_selecionada}",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("""
    ℹ️ **Nenhuma coluna booleana detectada automaticamente.**
    
    Colunas booleanas geralmente contêm:
    - Apenas 2 valores distintos (0/1, Sim/Não, True/False)
    - Valores como S/N, Y/N, Yes/No
    """)
    
    # Opção para o usuário selecionar manualmente
    st.subheader("🎯 Análise de Coluna Específica")
    todas_colunas = df.columns.tolist()
    coluna_manual = st.selectbox(
        "Selecione uma coluna para analisar:",
        todas_colunas
    )
    
    if coluna_manual:
        # Gráfico de barras para a coluna selecionada
        contagem_valores = df[coluna_manual].value_counts().head(10)  # Top 10 valores
        
        fig_barras = px.bar(
            x=contagem_valores.index.astype(str),
            y=contagem_valores.values,
            title=f"Distribuição de {coluna_manual}",
            labels={'x': coluna_manual, 'y': 'Contagem'},
            color=contagem_valores.values,
            color_continuous_scale='Viridis'
        )
        fig_barras.update_layout(height=500)
        st.plotly_chart(fig_barras, use_container_width=True)

# ========== NAVEGAÇÃO ==========
st.markdown("---")
st.markdown("<div style='text-align: center'>", unsafe_allow_html=True)
if st.button("🏠 Voltar ao Menu Inicial", use_container_width=True):
    st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)