# FILE: pages/9_🔬_Agrupamento.py
"""
Clustering com K-Means - Análise de Agrupamentos
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title='Análise de Clusters - K-Means',
    page_icon='🔬',
    layout='wide',
    initial_sidebar_state='expanded'
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .cluster-box {
        border-left: 4px solid #ff6b6b;
        padding: 1rem;
        background-color: #f8f9fa;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .k-input {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Função principal da aplicação"""
    
    # Verificar se os dados estão carregados no session state
    if 'df' not in st.session_state or st.session_state.df.empty:
        st.error("❌ Dados não carregados. Por favor, volte à página principal para carregar o dataset.")
        
        st.markdown("---")
        st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
        if st.button("🏠 Voltar ao Menu Inicial"):
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Carregar dados do session state
    original_df = st.session_state.df.copy()
    
    # Cabeçalho profissional
    st.markdown('<div class="main-header">🔬 Análise de Clusters - Algoritmo K-Means</div>', 
                unsafe_allow_html=True)
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações do Modelo")
        
        # Informações do dataset
        st.subheader("📊 Informações do Dataset")
        st.write(f"**Amostras:** {original_df.shape[0]}")
        st.write(f"**Variáveis:** {original_df.shape[1]}")
        
        st.subheader("🎯 Escolha do Número de Clusters")
        
        # MÚLTIPLAS OPÇÕES PARA ESCOLHER K
        metodo_escolha = st.radio(
            "Como definir o número de clusters:",
            ["📊 Análise Automática", "🎯 Escolher Manualmente", "🔍 Testar Múltiplos Valores", "⌨️ Inserir Valor Direto"],
            help="Selecione como deseja determinar o número de clusters"
        )
        
        if metodo_escolha == "📊 Análise Automática":
            st.info("O sistema irá sugerir o melhor K baseado nas métricas")
            k_sugerido = st.slider('K Sugerido', 2, 10, 3)
            k = k_sugerido
            
        elif metodo_escolha == "🎯 Escolher Manualmente":
            k = st.number_input(
                'Número de Clusters (K)',
                min_value=2,
                max_value=20,
                value=4,
                step=1,
                help='Escolha livremente o número de clusters desejado'
            )
            
        elif metodo_escolha == "🔍 Testar Múltiplos Valores":
            k_min = st.number_input('K mínimo', 2, 10, 2)
            k_max = st.number_input('K máximo', 3, 15, 8)
            k = st.slider('K selecionado', k_min, k_max, 4)
        
        else:  # Inserir Valor Direto
            st.markdown('<div class="k-input">', unsafe_allow_html=True)
            k = st.number_input(
                '🔢 Digite o número de clusters:',
                min_value=2,
                max_value=50,
                value=5,
                step=1,
                key="k_direct_input",
                help='Insira qualquer número entre 2 e 50'
            )
            st.markdown('</div>', unsafe_allow_html=True)
            st.info(f"📊 Serão gerados {k} clusters")
        
        st.subheader("⚙️ Parâmetros Avançados")
        max_iter = st.slider(
            'Máximo de Iterações',
            min_value=100,
            max_value=1000,
            value=300,
            step=50
        )
        
        n_init = st.slider(
            'Número de Inicializações',
            min_value=5,
            max_value=20,
            value=10,
            help='Número de vezes que o algoritmo será executado com diferentes seeds'
        )
        
        st.subheader("🔧 Pré-processamento")
        normalize = st.checkbox(
            'Normalizar Dados',
            value=True,
            help='Recomendado quando as escalas das features são diferentes'
        )
        
        # Botão para aplicar as configurações
        st.markdown("---")
        if st.button("🚀 Aplicar Configurações e Gerar Clusters", type="primary", use_container_width=True):
            st.rerun()
        
        st.info("""
        **💡 Dica Profissional:**
        - **K Pequeno (2-4):** Segmentação macro
        - **K Médio (5-8):** Segmentação balanceada  
        - **K Grande (9+):** Micro-segmentação
        - Use Silhouette Score > 0.5 para clusters bem definidos
        """)
    
    # Campo adicional no corpo principal para inserir K rapidamente
    st.header("🎯 Configuração Rápida do Número de Clusters")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        k_rapido = st.number_input(
            "🔢 Número de Clusters (K):",
            min_value=2,
            max_value=50,
            value=k,
            step=1,
            key="k_quick_input",
            help="Altere este valor para gerar os gráficos com diferentes números de clusters"
        )
    
    with col2:
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Atualizar Gráficos", type="secondary", use_container_width=True):
            k = k_rapido
            st.rerun()
    
    with col3:
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Resetar", type="secondary", use_container_width=True):
            k = 4
            st.rerun()
    
    # Atualizar k com o valor do campo rápido se for diferente
    if k_rapido != k:
        k = k_rapido
        st.info(f"🔄 Número de clusters atualizado para: **{k}**")
    
    # Mostrar o K atual sendo usado
    st.success(f"🎯 **Número de clusters ativo:** {k}")
    
    # Pré-processamento dos dados
    st.header("🔧 Pré-processamento dos Dados")
    
    # Limpar e preparar dados numéricos
    original_df.columns = original_df.columns.str.strip().str.replace('\n', ' ')
    numeric_df = original_df.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        st.error("❌ Nenhuma coluna numérica encontrada no dataset.")
        st.info("💡 O K-Means requer variáveis numéricas para funcionar.")
        return
    
    # Remover colunas com muitos valores missing
    threshold = 0.3  # 30% de valores missing
    numeric_df = numeric_df.dropna(axis=1, thresh=int(len(numeric_df) * (1 - threshold)))
    
    if numeric_df.shape[1] < 2:
        st.error("❌ Dados numéricos insuficientes para análise (mínimo 2 colunas)")
        st.info(f"💡 Colunas numéricas disponíveis: {numeric_df.shape[1]}")
        return
    
    # Preencher valores missing
    numeric_df = numeric_df.fillna(numeric_df.median())
    
    # Mostrar informações do pré-processamento
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Colunas Numéricas", f"{numeric_df.shape[1]}")
    with col2:
        st.metric("Amostras", f"{numeric_df.shape[0]}")
    with col3:
        st.metric("Valores Missing", "0" if not numeric_df.isnull().any().any() else "Sim")
    
    # Seleção de features para visualização
    st.subheader("🎯 Seleção de Features para Visualização")
    
    col1, col2 = st.columns(2)
    with col1:
        x_feature = st.selectbox("Feature para Eixo X:", numeric_df.columns, index=0)
    with col2:
        y_feature = st.selectbox("Feature para Eixo Y:", numeric_df.columns, index=min(1, len(numeric_df.columns)-1))
    
    # Normalização opcional
    if normalize:
        scaler = StandardScaler()
        analysis_data = scaler.fit_transform(numeric_df)
        analysis_data = pd.DataFrame(analysis_data, columns=numeric_df.columns)
    else:
        analysis_data = numeric_df.copy()
    
    # Análise de Clusters Ótimos (só mostra se K não for muito grande)
    if k <= 15:
        st.header("📊 Análise de Clusters Ótimos")
        
        def find_optimal_clusters(data, max_k=15):
            """Encontra o número ótimo de clusters usando método do cotovelo"""
            inertias = []
            silhouette_scores = []
            k_range = range(2, min(max_k + 1, 16))
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, k_val in enumerate(k_range):
                status_text.text(f"Calculando para K={k_val}...")
                kmeans = KMeans(n_clusters=k_val, random_state=42, n_init=10)
                labels = kmeans.fit_predict(data)
                inertias.append(kmeans.inertia_)
                
                if len(set(labels)) > 1:
                    silhouette_scores.append(silhouette_score(data, labels))
                else:
                    silhouette_scores.append(0)
                
                progress_bar.progress((i + 1) / len(k_range))
            
            progress_bar.empty()
            status_text.empty()
            
            return inertias, silhouette_scores, k_range
        
        with st.spinner('Calculando métricas de otimização...'):
            inertias, silhouette_scores, k_range = find_optimal_clusters(analysis_data, max_k=min(15, k+5))
        
        # Encontrar K ótimo baseado em Silhouette Score
        if silhouette_scores:
            optimal_k_silhouette = k_range[np.argmax(silhouette_scores)]
        else:
            optimal_k_silhouette = 3
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico do Cotovelo
            fig_elbow = px.line(
                x=list(k_range), 
                y=inertias,
                title='Método do Cotovelo - Inércia vs Número de Clusters',
                labels={'x': 'Número de Clusters (K)', 'y': 'Inércia'},
                markers=True
            )
            fig_elbow.add_vline(x=k, line_dash="dash", line_color="red", 
                               annotation_text=f"K selecionado: {k}")
            
            if len(inertias) > 1:
                differences = np.diff(inertias)
                second_diff = np.diff(differences)
                if len(second_diff) > 0:
                    optimal_k_elbow = np.argmax(second_diff) + 3
                    fig_elbow.add_vline(x=optimal_k_elbow, line_dash="dot", line_color="green",
                                      annotation_text=f"Sugestão: K={optimal_k_elbow}")
            
            fig_elbow.update_traces(line=dict(width=3))
            st.plotly_chart(fig_elbow, use_container_width=True)
        
        with col2:
            # Gráfico Silhouette Score
            fig_silhouette = px.line(
                x=list(k_range), 
                y=silhouette_scores,
                title='Silhouette Score vs Número de Clusters',
                labels={'x': 'Número de Clusters (K)', 'y': 'Silhouette Score'},
                markers=True
            )
            fig_silhouette.add_vline(x=k, line_dash="dash", line_color="red",
                                    annotation_text=f"K selecionado: {k}")
            fig_silhouette.add_vline(x=optimal_k_silhouette, line_dash="dot", line_color="green",
                                   annotation_text=f"Melhor K: {optimal_k_silhouette}")
            fig_silhouette.update_traces(line=dict(width=3))
            st.plotly_chart(fig_silhouette, use_container_width=True)
        
        # Mostrar recomendação
        st.info(f"""
        **🎯 Recomendação do Sistema:**
        - **Melhor K pelo Silhouette:** {optimal_k_silhouette} clusters
        - **Silhouette Score máximo:** {max(silhouette_scores):.3f}
        - **K selecionado:** {k} clusters
        """)
    else:
        st.info("📊 **Análise de clusters ótimos:** Disponível apenas para K ≤ 15")
    
    # Aplicar K-Means com o K escolhido
    st.header(f"🎯 Resultados do Clustering com K={k}")
    
    with st.spinner(f'Aplicando K-Means com K={k}...'):
        kmeans = KMeans(n_clusters=k, random_state=42, max_iter=max_iter, n_init=n_init)
        cluster_labels = kmeans.fit_predict(analysis_data)
    
    # Calcular Silhouette Score para o K selecionado
    if len(set(cluster_labels)) > 1:
        silhouette_avg = silhouette_score(analysis_data, cluster_labels)
    else:
        silhouette_avg = 0
    
    # Métricas de avaliação
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        inertia = kmeans.inertia_
        st.metric("Inércia Total", f"{inertia:,.2f}")
    
    with col2:
        st.metric("Silhouette Score", f"{silhouette_avg:.3f}")
    
    with col3:
        st.metric("Clusters Criados", k)
    
    with col4:
        st.metric("Iterações", kmeans.n_iter_)
    
    # Avaliação da qualidade
    if silhouette_avg > 0.7:
        st.success("✅ **Excelente segmentação!** Clusters muito bem definidos.")
    elif silhouette_avg > 0.5:
        st.success("✅ **Boa segmentação!** Clusters razoavelmente definidos.")
    elif silhouette_avg > 0.25:
        st.warning("⚠️ **Segmentação aceitável.** Clusters com alguma sobreposição.")
    else:
        st.error("❌ **Segmentação fraca.** Considere ajustar o número de clusters.")
    
    # Visualização dos resultados
    st.subheader("📈 Visualização dos Clusters")
    
    # Scatter plot 2D
    if x_feature != y_feature:
        plot_df = pd.DataFrame({
            x_feature: analysis_data[x_feature],
            y_feature: analysis_data[y_feature],
            'Cluster': cluster_labels.astype(str)
        })
        
        fig_scatter = px.scatter(
            plot_df,
            x=x_feature,
            y=y_feature,
            color='Cluster',
            title=f'Clusters K-Means (K={k}) - {x_feature} vs {y_feature}',
            labels={'color': 'Cluster'},
            template='plotly_white'
        )
        fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("⚠️ Selecione features diferentes para melhor visualização")
    
    # Distribuição e Centroides
    col1, col2 = st.columns(2)
    
    with col1:
        cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
        fig_dist = px.bar(
            x=cluster_counts.index,
            y=cluster_counts.values,
            title=f'Distribuição dos {k} Clusters',
            labels={'x': 'Cluster', 'y': 'Número de Amostras'},
            color=cluster_counts.index.astype(str),
            template='plotly_white'
        )
        fig_dist.update_layout(showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Centroides
        centroids = kmeans.cluster_centers_
        if not normalize:
            centroids_df = pd.DataFrame(centroids, columns=analysis_data.columns)
        else:
            centroids_original = scaler.inverse_transform(centroids)
            centroids_df = pd.DataFrame(centroids_original, columns=numeric_df.columns)
        
        centroids_df.index = [f'Cluster {i}' for i in range(k)]
        st.subheader(f"📍 Centroides dos {k} Clusters")
        st.dataframe(centroids_df.style.format("{:.2f}"), use_container_width=True)
    
    # Resto do código permanece igual...
    # Insights dos Clusters
    st.header("💡 Insights dos Clusters")
    
    # Adicionar labels ao dataframe original para análise
    original_df['Cluster'] = cluster_labels
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📋 Características dos {k} Clusters")
        for cluster_id in range(k):
            cluster_size = len(original_df[original_df['Cluster'] == cluster_id])
            cluster_percentage = (cluster_size / len(original_df)) * 100
            
            with st.expander(f"🔷 Cluster {cluster_id} - {cluster_size} amostras ({cluster_percentage:.1f}%)"):
                cluster_data = original_df[original_df['Cluster'] == cluster_id]
                
                if not cluster_data[numeric_df.columns].empty:
                    means = cluster_data[numeric_df.columns].mean()
                    top_features = means.nlargest(3)
                    st.write("**Características principais:**")
                    for feature, value in top_features.items():
                        st.write(f"- {feature}: {value:.2f}")
                    
                    overall_means = numeric_df.mean()
                    st.write("**Comparação com média geral:**")
                    for feature in top_features.index:
                        diff = means[feature] - overall_means[feature]
                        st.write(f"- {feature}: {diff:+.2f} vs média geral")
    
    with col2:
        st.subheader("🎯 Estratégias Recomendadas")
        
        if k == 2:
            st.success("""
            **Segmentação Binária Ideal para:**
            - Estratégias de marketing A/B
            - Segmentação básica (Alto/Baixo)
            - Análises de performance simples
            """)
        elif 3 <= k <= 4:
            st.info("""
            **Segmentação Balanceada Ideal para:**
            - Estratégias Bronze/Prata/Ouro
            - Níveis de serviço diferenciados
            - Programas de fidelidade
            """)
        elif 5 <= k <= 7:
            st.warning("""
            **Segmentação Detalhada Ideal para:**
            - Marketing de precisão
            - Personalização avançada
            - Micro-segmentação de mercado
            """)
        else:
            st.error("""
            **Segmentação Complexa:**
            - Requer análise muito detalhada
            - Ideal para pesquisa avançada
            - Pode ser muito específica
            """)
        
        st.info(f"""
        **📊 Com {k} clusters você pode:**
        - Criar {k} estratégias de marketing distintas
        - Desenvolver {k} níveis de produto/serviço
        - Segmentar em {k} perfis de cliente
        """)
    
    # Download dos resultados
    st.header("📥 Exportar Resultados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = original_df.to_csv(index=False)
        st.download_button(
            label="📊 Baixar Dados com Clusters (CSV)",
            data=csv,
            file_name=f"clustering_results_k{k}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        report_text = f"""
        RELATÓRIO DE CLUSTERING K-MEANS
        ==============================
        Dataset: {st.session_state.get('uploaded_file_name', 'food.xlsx')}
        Clusters (K): {k}
        Amostras: {len(original_df)}
        Silhouette Score: {silhouette_avg:.3f}
        Inércia: {inertia:,.2f}
        
        DISTRIBUIÇÃO DOS CLUSTERS:
        """
        for cluster_id in range(k):
            count = len(original_df[original_df['Cluster'] == cluster_id])
            percentage = (count / len(original_df)) * 100
            report_text += f"\nCluster {cluster_id}: {count} amostras ({percentage:.1f}%)"
        
        st.download_button(
            label="📄 Baixar Relatório (TXT)",
            data=report_text,
            file_name=f"clustering_report_k{k}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # BOTÃO DE VOLTAR NO PADRÃO SOLICITADO
    st.markdown("---")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("🏠 Voltar ao Menu Inicial"):
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Rodapé profissional
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔬 Análise de Clusters K-Means • Desenvolvido para Insights de Dados</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()