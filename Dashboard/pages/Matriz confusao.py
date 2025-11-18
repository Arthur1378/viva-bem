"""
Tela 11 — Matriz de Confusão Estilizada
Versão: integrada com seletor de target quando não definido no session_state
Autor: Gerado por ChatGPT para Leandro
"""
import io
import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Matriz de Confusão", layout="wide")
st.title("📊 Matriz de Confusão")

# -----------------------------------------------------------
# VERIFICAÇÃO DOS DADOS + SELETOR DE TARGET
# -----------------------------------------------------------

def verificar_dados():
    """Verifica se os dados estão em session_state. Se não, interrompe a execução."""
    if "df" not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error(
            """
        📝 **Dados não encontrados!**
        Por favor, volte à página inicial e carregue seus dados.
        """
        )
        if st.button("🏠 Voltar ao Dashboard"):
            st.switch_page("app.py")
        st.stop()
    df_local = st.session_state.df.copy()
    return df_local

df = verificar_dados()

# Se target não estiver definido
if "target_column" not in st.session_state or not st.session_state.target_column:
    st.warning("🎯 Nenhum target definido. Você pode selecionar aqui mesmo:")
    possible_targets = list(df.columns)
    selected_target = st.selectbox("Selecione a coluna target:", options=possible_targets, index=0)
    col_confirm, col_note = st.columns([1, 3])
    with col_confirm:
        if st.button("Confirmar Target"):
            st.session_state.target_column = selected_target
            st.success(f"Target definido como: {selected_target}")
            st.rerun()
    with col_note:
        st.info("Se preferir, defina a variável target na página inicial antes de acessar esta tela.")

target_column = st.session_state.get("target_column")

if target_column not in df.columns:
    st.error(f"❌ A coluna target '{target_column}' não existe no dataset.")
    if st.button("🏠 Voltar ao Dashboard"):
        st.switch_page("app.py")
    st.stop()

# -----------------------------------------------------------
# CABEÇALHO INFORMATIVO
# -----------------------------------------------------------

st.success(f"✅ **Dataset carregado:** {st.session_state.get('uploaded_file_name', 'Seu arquivo')}")
st.success(f"🎯 **Variável target:** {target_column}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Amostras", len(df))
with col2:
    st.metric("Total de Features", len(df.columns) - 1)
with col3:
    st.metric("Classes do Target", df[target_column].nunique())
with col4:
    nulos_target = df[target_column].isna().sum()
    st.metric("Valores Nulos no Target", nulos_target)

# -----------------------------------------------------------
# CONTROLES DE MODELO E VISUALIZAÇÃO
# -----------------------------------------------------------

with st.expander("⚙️ Configurações do Modelo e Visualização", expanded=True):
    st.subheader("🔍 Seleção de Features")
    features_disponiveis = [col for col in df.columns if col != target_column]
    features_selecionadas = st.multiselect(
        "Selecionar Features para o Modelo:",
        options=features_disponiveis,
        default=features_disponiveis[: min(4, len(features_disponiveis))],
    )

    if not features_selecionadas:
        st.error("⚠️ Selecione pelo menos uma feature para treinar o modelo.")
        st.stop()

    st.subheader("🎯 Parâmetros do Modelo")
    test_size = st.slider("Proporção para Teste:", 0.1, 0.5, 0.3, 0.05)
    n_estimators = st.slider("Número de Árvores:", 10, 300, 100, 10)
    max_depth = st.slider("Profundidade Máxima:", 2, 20, 8, 1)

    st.subheader("🎨 Visualização da Matriz")
    normalizacao = st.selectbox(
        "Normalização da Matriz:", ["Nenhuma", "True (por linha)", "Pred (por coluna)", "All (por total)"]
    )
    escala_cores = st.selectbox(
        "Escala de Cores:", ["Blues", "Viridis", "Plasma", "Reds", "Greens", "Teal"]
    )
    mostrar_valores = st.radio("Mostrar valores como:", ["Números Absolutos", "Percentuais"])
    destacar_erros = st.checkbox("Destacar células de erro", value=True)

# -----------------------------------------------------------
# AGRUPAMENTO DE CLASSES PEQUENAS
# -----------------------------------------------------------

with st.expander("🧩 Agrupamento de Classes Pequenas", expanded=False):
    limiar_minimo = st.number_input(
        "Aglomerar classes com menos de X amostras em 'Outros':", min_value=1, max_value=50, value=2
    )

df_work = df.copy()
target_counts = df_work[target_column].value_counts()
classes_raras = target_counts[target_counts < limiar_minimo].index.tolist()

if len(classes_raras) > 0:
    df_candidate = df_work.copy()
    df_candidate[target_column] = df_candidate[target_column].apply(lambda x: "Outros" if x in classes_raras else x)
    if df_candidate[target_column].nunique() > 1:
        df_work = df_candidate
        st.info(f"🔎 Classes agrupadas em 'Outros': {len(classes_raras)}")

# -----------------------------------------------------------
# TREINAMENTO DO MODELO
# -----------------------------------------------------------

try:
    with st.spinner("🔄 Preparando dados e treinando modelo..."):
        X = df_work[features_selecionadas].copy()
        y = df_work[target_column].copy()

        # 🔥 Usar apenas colunas numéricas
        X = X.select_dtypes(include=["number"])
        if X.shape[1] == 0:
            st.error("❌ Todas as features selecionadas são não-numéricas.")
            st.stop()

        mask = X.notna().all(axis=1) & y.notna()
        X = X[mask]
        y = y[mask]
        if len(X) == 0:
            st.error("❌ Não há dados válidos após remover valores nulos.")
            st.stop()

        # Codificar target
        y = y.astype(str)
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        class_labels = list(le.classes_)

        # Garantir pelo menos 2 classes
        if len(np.unique(y_encoded)) < 2:
            st.error("❌ O target precisa ter pelo menos 2 classes distintas.")
            st.stop()

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=42, stratify=y_encoded
        )

        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        accuracy = model.score(X_test, y_test)

        cv_folds = 5 if len(X) >= 5 else 2
        try:
            scores_cv = cross_val_score(model, X, y_encoded, cv=cv_folds)
        except Exception:
            scores_cv = np.array([accuracy])

    st.success(f"✅ Modelo treinado com sucesso! Acurácia: {accuracy:.2%}")

except Exception as e:
    st.error(f"❌ Erro durante o treinamento: {str(e)}")
    st.stop()

# -----------------------------------------------------------
# MATRIZ DE CONFUSÃO
# -----------------------------------------------------------

st.subheader("🎨 Matriz de Confusão")

# Garantir class_labels compatível com cm
class_labels = class_labels[:cm.shape[0]]

cm_normalized = cm.astype("float")
cm_display = cm_normalized.copy()
text_suffix = ""

if normalizacao == "True (por linha)":
    row_sums = cm_normalized.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    cm_display = (cm_normalized / row_sums) * 100
    text_suffix = "%"
elif normalizacao == "Pred (por coluna)":
    col_sums = cm_normalized.sum(axis=0, keepdims=True)
    col_sums[col_sums == 0] = 1
    cm_display = (cm_normalized / col_sums) * 100
    text_suffix = "%"
elif normalizacao == "All (por total)":
    total = cm_normalized.sum()
    total = total if total > 0 else 1
    cm_display = (cm_normalized / total) * 100
    text_suffix = "%"

if mostrar_valores == "Percentuais" and normalizacao != "Nenhuma":
    text_matrix = np.round(cm_display, 1).astype(str)
    text_matrix = np.core.defchararray.add(text_matrix, text_suffix)
else:
    text_matrix = cm.astype(int).astype(str)

colorscale = (
    [[0, "lightcoral"], [0.3, "lightyellow"], [0.7, "lightblue"], [1, "darkblue"]]
    if destacar_erros
    else escala_cores.lower()
)

fig = go.Figure(
    data=go.Heatmap(
        z=cm_display,
        x=class_labels,
        y=class_labels,
        colorscale=colorscale,
        text=text_matrix,
        texttemplate="%{text}",
        textfont={"size": 14, "color": "white"},
        hoverinfo="text",
    )
)

normalize_text = {
    "Nenhuma": "Valores Absolutos",
    "True (por linha)": "Normalizada por Linha (%)",
    "Pred (por coluna)": "Normalizada por Coluna (%)",
    "All (por total)": "Normalizada por Total (%)",
}

fig.update_layout(
    title=f"Matriz de Confusão - {normalize_text.get(normalizacao, normalizacao)}",
    xaxis_title="Rótulo Predito",
    yaxis_title="Rótulo Verdadeiro",
    height=500,
    width=600,
    font=dict(size=12),
)

st.plotly_chart(fig, width="stretch")

# -----------------------------------------------------------
# MÉTRICAS E IMPORTÂNCIA DAS FEATURES
# -----------------------------------------------------------

st.subheader("🎯 Importância das Features no Modelo")
features_corrigidas = features_selecionadas[: len(model.feature_importances_)]
importance_df = pd.DataFrame({
    "Feature": features_corrigidas,
    "Importância": model.feature_importances_
}).sort_values(by="Importância", ascending=False)

fig_importance = go.Figure(
    go.Bar(
        x=importance_df["Importância"],
        y=importance_df["Feature"],
        orientation="h",
        text=importance_df["Importância"].apply(lambda x: f"{x:.3f}"),
        textposition="auto",
    )
)
fig_importance.update_layout(
    title="Importância das Features no Modelo",
    xaxis_title="Importância",
    yaxis_title="Features",
    height=400,
)
st.plotly_chart(fig_importance, width="stretch")
st.dataframe(importance_df, width="stretch")

# -----------------------------------------------------------
# EXPORTAÇÃO DE RESULTADOS
# -----------------------------------------------------------

st.markdown("---")
st.subheader("💾 Exportar Resultados")

report_data = {
    "performance_geral": {
        "acuracia": float(accuracy),
        "acuracia_cv_media": float(scores_cv.mean()),
        "acuracia_cv_std": float(scores_cv.std()),
        "total_amostras_teste": int(len(X_test)),
        "numero_classes": int(len(class_labels)),
    },
    "importancia_features": importance_df.to_dict("records"),
}

report_json = json.dumps(report_data, indent=2, ensure_ascii=False)

st.download_button(
    label="📥 Baixar Relatório (JSON)",
    data=report_json,
    file_name="relatorio_matriz_confusao.json",
    mime="application/json",
)

output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    pd.DataFrame(cm, columns=class_labels, index=class_labels).to_excel(writer, sheet_name="Matriz_Confusao")
    importance_df.to_excel(writer, sheet_name="Importancia_Features", index=False)
st.download_button(
    label="📥 Baixar Dados (Excel)",
    data=output.getvalue(),
    file_name="analise_matriz_confusao.xlsx",
    mime="application/vnd.ms-excel",
)

# -----------------------------------------------------------
# BOTÃO VOLTAR
# -----------------------------------------------------------

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🏠 Voltar ao Dashboard Principal", width="stretch"):
        st.switch_page("app.py")
