import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# -----------------------------------------------------------
# FUNÇÃO COM CACHE PARA CARREGAR O DATASET
# -----------------------------------------------------------

@st.cache_data
def carregar_dados(uploaded_file):
    """Carrega o dataset a partir do arquivo uploadado"""
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            st.error("Formato de arquivo não suportado. Use .xlsx ou .csv")
            return pd.DataFrame()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()

# -----------------------------------------------------------
# UPLOAD DO ARQUIVO E CARREGAMENTO DOS DADOS
# -----------------------------------------------------------

st.title("📈 Dashboard de Análises de Dados")

# Verifica se já temos dados carregados
dados_carregados = 'df' in st.session_state and not st.session_state.df.empty

if not dados_carregados:
    # Upload do arquivo apenas se não tiver dados carregados
    uploaded_file = st.file_uploader(
        "Faça upload do seu arquivo de dados", 
        type=['xlsx', 'csv'],
        help="Suporta arquivos Excel (.xlsx) e CSV (.csv)"
    )
    
    if uploaded_file is not None:
        with st.spinner('Carregando dados...'):
            st.session_state.df = carregar_dados(uploaded_file)
            st.session_state.uploaded_file_name = uploaded_file.name
        st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
        st.rerun()
else:
    # Mostra informações do arquivo já carregado
    st.success(f"✅ Arquivo carregado: {st.session_state.get('uploaded_file_name', 'Arquivo')}")
    
    # Botão para recarregar outro arquivo
    if st.button("📤 Carregar outro arquivo"):
        # Limpa os dados do session state
        del st.session_state.df
        if 'uploaded_file_name' in st.session_state:
            del st.session_state.uploaded_file_name
        st.rerun()

# -----------------------------------------------------------
# PROCESSAMENTO DOS DADOS (se estiverem carregados)
# -----------------------------------------------------------

if 'df' in st.session_state and not st.session_state.df.empty:
    df = st.session_state.df
    
    # -----------------------------------------------------------
    # RESUMO DO DATASET
    # -----------------------------------------------------------
    
    st.subheader("📊 Resumo do Dataset")
    
    num_linhas = df.shape[0]
    num_colunas = df.shape[1]
    num_nulos = df.isna().sum().sum()
    num_duplicados = df.duplicated().sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Linhas**")
        st.markdown(f"<h2>{num_linhas}</h2>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Colunas**")
        st.markdown(f"<h2>{num_colunas}</h2>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("**Nulos**")
        st.markdown(f"<h2>{num_nulos}</h2>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("**Duplicatas**")
        st.markdown(f"<h2>{num_duplicados}</h2>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # -----------------------------------------------------------
    # MENU PRINCIPAL CUSTOMIZADO
    # -----------------------------------------------------------
    
    st.subheader("Escolha uma opção abaixo:")
    
    TELAS = {
        "Dataframes": "Dataframes",
        "Filtros DataFrame": "Filtros",
        "Agrupamentos DataFrames": "Agrupamentos",
        "Booleans": "Boolean",
        "Profiling": "Profiling",
        "Arquivos Parquet": "Parquet",
        "Plots": "Plots",
        "Subplots": "Subplots",
        "Agrupamento": "K-means",
        "Classificação": "Classificacao",
        "Matriz Confusão": "Matriz confusao"
    }
    
    # Layout dos botões (3 colunas)
    cols = st.columns(3)
    
    for i, (label, pagina) in enumerate(TELAS.items()):
        with cols[i % 3]:
            if st.button(label, use_container_width=True):
                st.query_params["page"] = pagina
                st.rerun()
    
    # -----------------------------------------------------------
    # ROTEAMENTO ENTRE PÁGINAS
    # -----------------------------------------------------------
    
    pagina = st.query_params.get("page", None)
    
    if pagina:
        st.switch_page(f"pages/{pagina}.py")

elif 'df' in st.session_state and st.session_state.df.empty:
    st.error("O arquivo carregado está vazio. Por favor, carregue outro arquivo.")
    if st.button("🔄 Tentar novamente"):
        del st.session_state.df
        st.rerun()
else:
    st.info("👆 Por favor, faça upload de um arquivo Excel (.xlsx) ou CSV (.csv) para começar.")