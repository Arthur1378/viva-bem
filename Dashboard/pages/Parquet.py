# FILE: pages/6_📦_Arquivos_Parquet.py
"""
Tela 6 — Parquet demo
"""
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title='Parquet', layout='wide')
st.title('📦 Arquivos Parquet')

# Verifica se os dados estão carregados
if 'df' not in st.session_state:
    st.error("📝 **Nenhum dado carregado!**")
    st.info("Por favor, volte ao menu principal e carregue seus dados primeiro.")
    st.markdown("---")
    if st.button("🏠 Voltar ao Menu Inicial", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

# Carrega os dados do session state
df = st.session_state.df

# Header informativo
st.success(f"✅ **Dados carregados com sucesso!** ({df.shape[0]} linhas × {df.shape[1]} colunas)")

# Mostrar dados
st.subheader("📊 Visualização dos Dados")
st.dataframe(df.head(), use_container_width=True)

# Estatísticas rápidas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Linhas", df.shape[0])
with col2:
    st.metric("Total de Colunas", df.shape[1])
with col3:
    st.metric("Tamanho na Memória", f"{df.memory_usage(deep=True).sum() // 1024} KB")

# Configurações de exportação
st.markdown("---")
st.subheader("💾 Configurações de Exportação Parquet")

col1, col2, col3 = st.columns(3)

with col1:
    compression = st.selectbox(
        "Método de Compressão",
        ['snappy', 'gzip', 'brotli', 'none'],
        help="snappy: rápido | gzip: boa compressão | brotli: alta compressão"
    )

with col2:
    filename = st.text_input("Nome do arquivo", "dados_exportados.parquet")

with col3:
    include_index = st.checkbox("Incluir índice", value=False, help="Incluir coluna de índice no arquivo")

# Botão de exportação
st.markdown("---")
st.subheader("🚀 Exportar Arquivo")

if st.button("📦 Gerar Arquivo Parquet", type="primary", use_container_width=True):
    try:
        # Criar arquivo em memória
        buffer = BytesIO()
        df.to_parquet(
            buffer, 
            index=include_index, 
            compression=compression,
            engine='pyarrow'
        )
        buffer.seek(0)
        
        # Informações do arquivo
        file_size = len(buffer.getvalue())
        
        # Botão de download
        st.download_button(
            label=f"⬇️ Baixar {filename} ({file_size // 1024} KB)",
            data=buffer,
            file_name=filename,
            mime="application/octet-stream",
            use_container_width=True
        )
        
        # Estatísticas de compressão
        st.success("✅ Arquivo Parquet gerado com sucesso!")
        
        # Comparação de tamanhos (opcional)
        with st.expander("📈 Comparação com outros formatos"):
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=include_index)
            csv_size = len(csv_buffer.getvalue())
            
            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=include_index)
            excel_size = len(excel_buffer.getvalue())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                reduction = ((csv_size - file_size) / csv_size) * 100
                st.metric("CSV", f"{csv_size // 1024} KB", f"-{reduction:.1f}%")
            with col2:
                st.metric("Parquet", f"{file_size // 1024} KB")
            with col3:
                reduction_excel = ((excel_size - file_size) / excel_size) * 100
                st.metric("Excel", f"{excel_size // 1024} KB", f"-{reduction_excel:.1f}%")
                
    except Exception as e:
        st.error(f"❌ Erro ao gerar arquivo Parquet: {str(e)}")

# Seção educacional
st.markdown("---")
st.subheader("🎓 Sobre o Formato Parquet")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **✅ Vantagens:**
    - ⚡ **Rápido**: Leitura/escrita otimizada
    - 💾 **Compacto**: Compressão eficiente
    - 🏗️ **Estruturado**: Preserva tipos de dados
    - 🔍 **Busca eficiente**: Filtragem por colunas
    - ☁️ **Ideal para Big Data**
    """)

with col2:
    st.markdown("""
    **📊 Melhor para:**
    - Análises com grandes volumes
    - Processamento em lote (batch)
    - Armazenamento em data lakes
    - Dados que não mudam frequentemente
    - Integração com Spark/Pandas
    """)

# Navegação
st.markdown("---")
st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
if st.button("🏠 Voltar ao Menu Inicial", use_container_width=True):
    st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)