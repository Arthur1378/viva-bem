# FILE: pages/10_🧠_Classificação.py
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title='Classificação', layout='wide')
st.title('🧠 Classificação — Modelo Random Forest')

# ----------------------------
# 1) Carregar dados
# ----------------------------
if 'df' not in st.session_state or st.session_state.df.empty:
    st.error("📊 Dataset não encontrado. Volte à página inicial e carregue os dados.")
    st.stop()

df = st.session_state.df
st.success(f"✅ Dataset carregado: {len(df)} linhas × {len(df.columns)} colunas")

# ----------------------------
# 2) Seleção da coluna alvo
# ----------------------------
target_column = st.selectbox("Selecione a coluna para classificação:", df.columns)

# Análise da coluna alvo
st.write(f"**Análise da coluna '{target_column}':**")
st.write(f"- Tipo: {df[target_column].dtype}")
st.write(f"- Valores únicos: {df[target_column].nunique()}")
st.write(f"- Valores não nulos: {df[target_column].count()}/{len(df)}")

# Distribuição
if df[target_column].nunique() <= 20:
    fig_dist = px.bar(x=df[target_column].value_counts().index, 
                     y=df[target_column].value_counts().values,
                     title="Distribuição das Classes",
                     labels={'x': 'Classe', 'y': 'Quantidade'})
    st.plotly_chart(fig_dist, width='stretch')
else:
    st.bar_chart(df[target_column].value_counts().head(15))

# ----------------------------
# 3) Pré-processamento
# ----------------------------
st.subheader("🔧 Pré-processamento")

df_clean = df.dropna(subset=[target_column]).copy()
if len(df_clean) < len(df):
    st.info(f"📝 Removidas {len(df) - len(df_clean)} linhas com valores nulos")

y = df_clean[target_column]
X = df_clean.drop(columns=[target_column])

# Verificações
if len(y) < 10:
    st.error("❌ Poucos dados para treinamento")
    st.stop()

if y.nunique() < 2:
    st.error("❌ Coluna alvo precisa ter pelo menos 2 classes")
    st.stop()

# Converter colunas categóricas
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()

st.write(f"- Colunas numéricas: {len(num_cols)}")
st.write(f"- Colunas categóricas: {len(cat_cols)}")

X_processed = X[num_cols].copy()
label_encoders = {}

if cat_cols:
    for col in cat_cols:
        try:
            le = LabelEncoder()
            encoded_values = le.fit_transform(X[col].astype(str))
            X_processed[col] = encoded_values
            label_encoders[col] = le
        except Exception as e:
            if col in X_processed.columns:
                X_processed = X_processed.drop(columns=[col])

# Preencher missing values
for col in X_processed.columns:
    if X_processed[col].isna().any():
        if X_processed[col].dtype in [np.float64, np.int64]:
            X_processed[col].fillna(X_processed[col].mean(), inplace=True)

st.write(f"📊 Shape final: {X_processed.shape}")

# ----------------------------
# 4) Configurações
# ----------------------------
st.subheader("⚙️ Configurações do Modelo")

col1, col2 = st.columns(2)
with col1:
    test_size = st.slider("Tamanho do teste:", 0.1, 0.5, 0.2, 0.05)
with col2:
    n_estimators = st.slider("Número de árvores:", 10, 100, 30, 5)

# ----------------------------
# 5) Treinamento
# ----------------------------
train_button = st.button("🎯 Treinar Modelo", type="primary")

if train_button:
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔍 Preparando dados...")
        progress_bar.progress(20)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=test_size, random_state=42
        )
        
        status_text.text("🌳 Configurando modelo...")
        progress_bar.progress(40)
        
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            n_jobs=-1
        )
        
        status_text.text("🚀 Treinando...")
        progress_bar.progress(70)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        status_text.text("📊 Calculando métricas...")
        progress_bar.progress(90)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        progress_bar.progress(100)
        status_text.text("✅ Completo!")
        
        # Salvar tudo no session_state para usar depois
        st.session_state.model_trained = True
        st.session_state.model = model
        st.session_state.X_processed = X_processed
        st.session_state.label_encoders = label_encoders
        st.session_state.importance_df = pd.DataFrame({
            'Feature': X_processed.columns,
            'Importância': model.feature_importances_
        }).nlargest(10, 'Importância')
        st.session_state.accuracy = accuracy
        st.session_state.precision = precision
        st.session_state.recall = recall
        st.session_state.f1 = f1
        st.session_state.y_test = y_test
        st.session_state.y_pred = y_pred
        st.session_state.X = X
        
        st.success("Modelo treinado com sucesso!")
        st.rerun()
            
    except Exception as e:
        st.error(f"❌ Erro no treinamento: {str(e)}")

# ----------------------------
# 6) MOSTRAR RESULTADOS SE O MODELO JÁ FOI TREINADO
# ----------------------------
if 'model_trained' in st.session_state and st.session_state.model_trained:
    
    # Recuperar variáveis do session_state
    model = st.session_state.model
    X_processed = st.session_state.X_processed
    label_encoders = st.session_state.label_encoders
    importance_df = st.session_state.importance_df
    accuracy = st.session_state.accuracy
    precision = st.session_state.precision
    recall = st.session_state.recall
    f1 = st.session_state.f1
    y_test = st.session_state.y_test
    y_pred = st.session_state.y_pred
    X = st.session_state.X
    
    # ----------------------------
    # ANÁLISES DE CLASSIFICAÇÃO
    # ----------------------------
    st.success("✅ Modelo treinado e pronto para uso!")
    
    # Métricas principais em cards
    st.subheader("📊 Métricas de Desempenho")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Acurácia", f"{accuracy:.1%}")
    col2.metric("Precisão", f"{precision:.1%}")
    col3.metric("Recall", f"{recall:.1%}")
    col4.metric("F1-Score", f"{f1:.1%}")
    
    # Gráfico de radar das métricas
    metrics = ['Acurácia', 'Precisão', 'Recall', 'F1-Score']
    values = [accuracy, precision, recall, f1]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=metrics,
        fill='toself',
        name='Desempenho'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title="Desempenho do Modelo - Radar Chart"
    )
    st.plotly_chart(fig_radar, width='stretch')
    
    # Relatório de classificação por classe
    st.subheader("🎯 Métricas por Classe")
    
    # Calcular métricas para cada classe
    unique_classes = np.unique(y_test)
    class_metrics = []
    
    for class_name in unique_classes:
        # Criar arrays binários para cada classe
        y_test_binary = (y_test == class_name)
        y_pred_binary = (y_pred == class_name)
        
        if sum(y_test_binary) > 0:  # Só calcular se houver amostras
            precision_class = precision_score(y_test_binary, y_pred_binary, zero_division=0)
            recall_class = recall_score(y_test_binary, y_pred_binary, zero_division=0)
            f1_class = f1_score(y_test_binary, y_pred_binary, zero_division=0)
            support = sum(y_test_binary)
            
            class_metrics.append({
                'Classe': str(class_name),
                'Precisão': precision_class,
                'Recall': recall_class,
                'F1-Score': f1_class,
                'Support': support
            })
    
    if class_metrics:
        metrics_df = pd.DataFrame(class_metrics)
        
        # Gráfico de métricas por classe
        fig_metrics = px.bar(metrics_df, 
                           x='Classe', 
                           y=['Precisão', 'Recall', 'F1-Score'],
                           title='Métricas por Classe',
                           barmode='group')
        st.plotly_chart(fig_metrics, width='stretch')
        
        # Gráfico de support por classe
        fig_support = px.bar(metrics_df, 
                           x='Classe', 
                           y='Support',
                           title='Número de Amostras por Classe (Support)',
                           color='Support',
                           color_continuous_scale='viridis')
        st.plotly_chart(fig_support, width='stretch')
    
    # Features importantes
    st.subheader("🔍 Features Mais Importantes")
    
    if len(X_processed.columns) > 0:
        fig_importance = px.bar(importance_df, 
                              x='Importância', 
                              y='Feature',
                              orientation='h',
                              title='Top 10 Features Mais Importantes',
                              color='Importância',
                              color_continuous_scale='viridis')
        st.plotly_chart(fig_importance, width='stretch')
    
    # ----------------------------
    # PREDIÇÃO INTERATIVA
    # ----------------------------
    st.subheader("🔮 Teste de Predição")
    
    if len(X_processed.columns) > 0:
        # Usar as 3 features mais importantes para o teste
        if len(importance_df) >= 3:
            top_features = importance_df.head(3)['Feature'].tolist()
        else:
            top_features = X_processed.columns[:3].tolist()
        
        st.write("**Ajuste os valores das principais features:**")
        
        manual_input = {}
        
        for i, feature in enumerate(top_features):
            st.write(f"**{feature}**")
            
            if feature in label_encoders:
                # Feature categórica - mostrar selectbox
                options = label_encoders[feature].classes_
                selected = st.selectbox(f"Selecione {feature}:", options, key=f"cat_{feature}")
                manual_input[feature] = label_encoders[feature].transform([selected])[0]
            else:
                # Feature numérica - mostrar slider
                min_val = float(X_processed[feature].min())
                max_val = float(X_processed[feature].max())
                avg_val = float(X_processed[feature].mean())
                
                manual_input[feature] = st.slider(
                    f"Valor para {feature}:", 
                    min_val, max_val, avg_val,
                    key=f"num_{feature}"
                )
        
        # Botão de predição SEPARADO - não reroda o script inteiro
        if st.button("🎯 Fazer Predição", type="primary", key="predict_button"):
            try:
                # Criar input completo
                test_input = {}
                for col in X_processed.columns:
                    if col in manual_input:
                        test_input[col] = manual_input[col]
                    elif col in label_encoders:
                        # Usar valor mais comum para colunas categóricas não selecionadas
                        test_input[col] = label_encoders[col].transform([X[col].mode()[0]])[0]
                    else:
                        # Usar média para colunas numéricas não selecionadas
                        test_input[col] = float(X_processed[col].mean())
                
                test_df = pd.DataFrame([test_input])
                test_df = test_df[X_processed.columns]  # Garantir ordem correta
                
                prediction = model.predict(test_df)[0]
                probabilities = model.predict_proba(test_df)[0]
                
                # Resultado com destaque
                st.success(f"**🎯 CLASSE PREVISTA: {prediction}**")
                
                # Gráfico de probabilidades
                prob_df = pd.DataFrame({
                    'Classe': model.classes_,
                    'Probabilidade': probabilities
                }).nlargest(8, 'Probabilidade')
                
                fig_proba = px.bar(prob_df, 
                                 x='Probabilidade', 
                                 y='Classe',
                                 orientation='h',
                                 title='Probabilidades por Classe (Top 8)',
                                 color='Probabilidade',
                                 color_continuous_scale='blues')
                fig_proba.update_layout(xaxis_range=[0, 1])
                st.plotly_chart(fig_proba, width='stretch')
                
                # Mostrar confiança da predição
                max_prob = prob_df['Probabilidade'].max()
                st.metric("Confiança da Predição", f"{max_prob:.1%}")
                
            except Exception as e:
                st.error(f"Erro na predição: {e}")
    else:
        st.info("ℹ️ Não há colunas disponíveis para teste")

# ----------------------------
# 7) Botão de voltar
# ----------------------------
st.markdown("---")
if st.button("← Voltar ao Menu Principal", use_container_width=True):
    st.switch_page("app.py")