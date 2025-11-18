# 🥗 **Viva Bem — Plataforma de Análise Nutricional com EDA, ML, Clusterização e Dashboard Interativo**

Projeto desenvolvido para a disciplina **PISI 3 — UFRPE**, integrando Análise Exploratória de Dados (EDA), modelos supervisionados e não supervisionados, explicabilidade com SHAP e um painel em Streamlit para predição nutricional.

O sistema permite explorar alimentos, treinar modelos, gerar insights e explicar cada decisão do modelo de forma global e local.

---

## 📌 **Índice**

1. Sobre o Projeto
2. Objetivos
3. Tecnologias Utilizadas
4. Estrutura do Projeto
5. Como Executar
6. EDA — Análise Exploratória
7. ML — Classificação e Regressão
8. Clusterização
9. SHAP — Explicabilidade Global e Local
10. Dashboard Interativo (Streamlit)
11. Dataset
12. **Resumo Técnico do Artigo**
13. **Contribuidores** (último item, como solicitado)

---

# 🎯 **1. Sobre o Projeto**

O **Viva Bem** é uma plataforma completa para análise nutricional, integrando:

* Exploracão de dados alimentares
* Modelos de classificação/regressão
* Clusterização nutricional
* Explicabilidade com SHAP
* Painel interativo para visualização e predição

---

# 🥅 **2. Objetivos**

## ✔ Técnicos

* EDA completa
* Testar diferentes algoritmos
* Balancear dados (SMOTEN)
* Normalizar e codificar variáveis
* Realizar tuning (GridSearch / RandomSearch)
* Comparar métricas
* Implementar clusterização (cotovelo + silhueta)
* Explicar decisões com SHAP global e local
* Construir painel Streamlit carregando o melhor modelo

## ✔ Acadêmicos

* Aplicar boas práticas de pré-processamento
* Documentar etapas do projeto
* Organizar o repositório com clareza
* Demonstrar conhecimentos da disciplina

---

# 🛠 **3. Tecnologias Utilizadas**

### Linguagem

* Python 3.10+

### Bibliotecas Principais

* pandas, numpy
* scikit-learn
* xgboost
* seaborn, matplotlib, plotly
* shap
* pyarrow (Parquet)
* streamlit

---

# 📂 **4. Estrutura do Projeto**

```
viva-bem/
│
├── Painel/                     → Aplicação Streamlit
├── imagens/                    → Gráficos e imagens
├── ml/                         → Scripts de Machine Learning
├── EDA/                        → Notebooks e scripts de EDA
├── Modelos de treinamento/     → Modelos exportados (.pkl)
├── Parquet/                    → Conversão e documentos parquet
├── Forma/                      → Scripts SHAP
│
├── Sobre parquet.md
├── food.cv.csv
├── LICENÇA
└── README.md
```

---

# 🚀 **5. Como Executar**

## 1️⃣ Clonar

```bash
git clone https://github.com/Arthur1378/viva-bem.git
cd viva-bem
```

## 2️⃣ Ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

# 📊 **6. EDA — Análise Exploratória**

Inclui:

* Conversão para Parquet
* Estatísticas descritivas
* Correlação
* Gráficos interativos
* Outliers e distribuição
* Tratamento de nulos

Executar:

```bash
python EDA/eda_food.py
```

---

# 🤖 **7. ML — Classificação e Regressão**

### ✔ Pré-processamento

* Normalização
* One-Hot Encoding
* Remoção de outliers
* **SMOTEN para balanceamento**
* Pipeline completo

### ✔ Modelos testados

* Random Forest
* XGBoost
* Gradient Boosting
* Regressão Logística
* SVM/KNN

### ✔ Tuning

* GridSearchCV
* RandomizedSearchCV

### ✔ Avaliação

* Acurácia
* Precisão/Recall/F1
* Matriz de confusão
* ROC/AUC
* Cross-validation

### ✔ Exportação

Salvos em `/Modelos de treinamento/`:

```
best_model.pkl
preprocessor.pkl
confusion_matrix.png
feature_importance.png
```

Rodar:

```bash
python ml/train_model.py
```

---

# 🔍 **8. Clusterização**

Inclui:

* K-Means
* Método do cotovelo
* Silhouette Score
* PCA para visualização
* Interpretação dos clusters nutricionais

Executar:

```bash
python ml/cluster_analysis.py
```

---

# 🧩 **9. SHAP — Explicabilidade**

### 🌎 Global

* SHAP Summary Plot (beeswarm)
* Feature Importance
* Barras por classe (multiclasse)

### 👤 Local (painel Streamlit)

* Force Plot mostrando contribuição de cada atributo para a previsão

Executar:

```bash
python Forma/shap_analysis.py
```

---

# 💻 **10. Dashboard Interativo (Streamlit)**

Inclui:

### 🥗 Classificação/Regressão

* Entrada pelo usuário
* Previsão
* Probabilidade
* Explicação local (SHAP)

### 📊 Módulos de análise

* Comparação de modelos
* Clusterização
* Visualizações de EDA
* Gráficos interativos

Executar o app:

```bash
streamlit run Painel/app.py
```

---

# 🥑 **11. Dataset**

* Base nutricional original `.csv`
* Convertida para Parquet para otimização (~80% menor)
* Arquivos e explicações em `/Parquet`

---

# 📘 **12. Resumo Técnico do Artigo (Resultados)**

Esta seção resume os achados científicos apresentados no relatório:

* A migração para **Parquet** reduziu ~80% do espaço e acelerou a EDA.
* A análise exploratória revelou padrões nutricionais importantes e correlações.
* O uso de **SMOTEN** corrigiu o desbalanceamento das classes.
* Após testar múltiplos algoritmos, o melhor modelo foi exportado e utilizado no painel.
* O tuning aprimorou as métricas sem causar overfitting (validado via cross-validation).
* A clusterização identificou grupos nutricionais coerentes, visualizados com PCA.
* A explicabilidade mostrou variáveis mais relevantes por classe e por previsão individual.

---

# 👥 **13. Contribuidores**


Projeto desenvolvido para a disciplina **PISI 3 — UFRPE**

**Integrantes:**

* Arthur Barbosa
* Carolinne Amorim
* Leandro Augusto
* Letícia Florêncio

**Orientação:** Gabriel Alves

---


