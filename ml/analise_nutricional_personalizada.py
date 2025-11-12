# ============================================================
# ARQUIVO: analise_nutricional_personalizada.py
# OBJETIVO: Gerar gráficos personalizados de análise nutricional
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------- CONFIGURAÇÕES GERAIS ---------------------

plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

# ------------------------- CARREGAR DADOS -------------------------

df = pd.read_csv('food.csv')

print("📊 DATASET CARREGADO COM SUCESSO!")
print(f"Shape: {df.shape}")
print(f"Colunas disponíveis: {list(df.columns)}")

# ------------------ SELEÇÃO E LIMPEZA ------------------

colunas_nutricionais = [
    'Data.Kilocalories', 'Data.Protein', 'Data.Fat.Total Lipid',
    'Data.Carbohydrate', 'Data.Fiber', 'Data.Major Minerals.Calcium',
    'Data.Cholesterol'
]

colunas_usar = [col for col in colunas_nutricionais if col in df.columns]
nutrientes_df = df[colunas_usar].copy()
nutrientes_df = nutrientes_df.fillna(nutrientes_df.median(numeric_only=True))
nutrientes_df['Category'] = df.get('Category', 'Desconhecida')
nutrientes_df['Description'] = df.get('Description', df.index.astype(str))

print(f"\n🔍 Analisando {len(nutrientes_df)} alimentos...\n")

# ============================================================
# GRÁFICOS PARA MARINA - SUBSTITUIÇÕES INTELIGENTES
# ============================================================

print("🏃‍♀️ GERANDO GRÁFICOS: Marina - Substituições Inteligentes")

plt.figure(figsize=(14, 8))

# Densidade nutricional
nutrientes_df['Densidade_Nutricional'] = (
    (nutrientes_df['Data.Protein'] + nutrientes_df.get('Data.Fiber', 0))
    / nutrientes_df['Data.Kilocalories'] * 100
)
top_densidade = nutrientes_df.nlargest(15, 'Densidade_Nutricional')

# Gráfico 1A
plt.subplot(1, 2, 1)
bars = plt.barh(
    [d[:25] + '...' if len(d) > 25 else d for d in top_densidade['Description']],
    top_densidade['Densidade_Nutricional'],
    color='lightgreen'
)
plt.xlabel('Densidade Nutricional (Proteína + Fibra por 100 kcal)')
plt.title('TOP 15 - Alimentos Mais Nutritivos (Marina)')
plt.gca().invert_yaxis()

for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.1f}',
             ha='left', va='center', fontsize=9)

# Gráfico 1B
plt.subplot(1, 2, 2)
scatter = plt.scatter(
    nutrientes_df['Data.Kilocalories'],
    nutrientes_df['Data.Protein'],
    alpha=0.7,
    c=nutrientes_df.get('Data.Fat.Total Lipid', 0),
    cmap='viridis'
)
plt.colorbar(scatter, label='Gordura Total (g)')
plt.xlabel('Calorias')
plt.ylabel('Proteína (g)')
plt.title('Relação Calorias x Proteína (Cores = Gordura)')
plt.tight_layout()
plt.show()

# ============================================================
# GRÁFICOS PARA CARLOS - FOCO EM PROTEÍNA
# ============================================================

print("\n💪 GERANDO GRÁFICOS: Carlos - Eficiência e Relação Proteica")

plt.figure(figsize=(14, 8))

# Eficiência proteica
nutrientes_df['Proteina_Por_Caloria'] = (
    nutrientes_df['Data.Protein'] / nutrientes_df['Data.Kilocalories'] * 100
)
top_eficiencia = nutrientes_df.nlargest(15, 'Proteina_Por_Caloria')

plt.subplot(1, 2, 1)
bars = plt.barh(
    [d[:25] + '...' if len(d) > 25 else d for d in top_eficiencia['Description']],
    top_eficiencia['Proteina_Por_Caloria'],
    color='skyblue'
)
plt.xlabel('Proteína por 100 Calorias (g)')
plt.title('Eficiência Proteica (Carlos)')
plt.gca().invert_yaxis()

# Relação proteína vs gordura
plt.subplot(1, 2, 2)
plt.scatter(
    nutrientes_df['Data.Protein'],
    nutrientes_df.get('Data.Fat.Total Lipid', 0),
    alpha=0.7,
    c=nutrientes_df['Data.Kilocalories'],
    cmap='plasma'
)
plt.colorbar(label='Calorias')
plt.xlabel('Proteína (g)')
plt.ylabel('Gordura (g)')
plt.title('Relação Proteína x Gordura')
plt.tight_layout()
plt.show()

# ============================================================
# GRÁFICOS PARA ANA - SAÚDE FAMILIAR (CÁLCIO)
# ============================================================

print("\n👨‍👩‍👧‍👦 GERANDO GRÁFICO: Ana - Alimentos Ricos em Cálcio")

if 'Data.Major Minerals.Calcium' in nutrientes_df.columns:
    plt.figure(figsize=(10, 8))
    top_calcio = nutrientes_df.nlargest(15, 'Data.Major Minerals.Calcium')

    plt.barh(
        [d[:30] + '...' if len(d) > 30 else d for d in top_calcio['Description']],
        top_calcio['Data.Major Minerals.Calcium'],
        color='lightcoral'
    )
    plt.xlabel('Cálcio (mg)')
    plt.title('TOP 15 - Alimentos com Mais Cálcio (Ana)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

# ============================================================
# GRÁFICOS PARA ROBERTO - CONTROLE GLICÊMICO
# ============================================================

print("\n🩺 GERANDO GRÁFICO: Roberto - Melhores Opções para Diabéticos")

if 'Data.Carbohydrate' in nutrientes_df.columns:
    plt.figure(figsize=(10, 8))

    nutrientes_df['Score_Diabetico'] = (
        nutrientes_df['Data.Protein'] / (nutrientes_df['Data.Carbohydrate'] + 1) * 10
    )
    top_diabetico = nutrientes_df.nlargest(12, 'Score_Diabetico')

    plt.barh(
        [d[:30] + '...' if len(d) > 30 else d for d in top_diabetico['Description']],
        top_diabetico['Score_Diabetico'],
        color='mediumpurple'
    )
    plt.xlabel('Score Diabético (Alta proteína / Baixo carboidrato)')
    plt.title('Melhores Opções para Diabéticos (Roberto)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

# ============================================================
# VISÃO GERAL - TOP 10 MAIS BALANCEADOS
# ============================================================

print("\n📊 GERANDO GRÁFICO: Comparativo Geral - Top 10 Balanceados")

plt.figure(figsize=(10, 8))
nutrientes_df['Balance_Score'] = (
    nutrientes_df['Data.Protein']
    - nutrientes_df.get('Data.Fat.Total Lipid', 0) * 0.5
    - nutrientes_df.get('Data.Carbohydrate', 0) * 0.3
    + nutrientes_df.get('Data.Fiber', 0) * 2
)
top_balanceados = nutrientes_df.nlargest(10, 'Balance_Score')

bars = plt.barh(
    [d[:30] + '...' if len(d) > 30 else d for d in top_balanceados['Description']],
    top_balanceados['Balance_Score'],
    color='gold'
)
plt.xlabel('Score de Balanceamento')
plt.title('TOP 10 - Alimentos Mais Balanceados (Visão Geral)')
plt.gca().invert_yaxis()

for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.1f}',
             ha='left', va='center', fontsize=9)

plt.tight_layout()
plt.show()

# ============================================================
# RESUMO FINAL
# ============================================================

print("\n" + "="*60)
print("🎉 TODOS OS GRÁFICOS GERADOS COM SUCESSO!")
print("="*60)
print("""
📋 RESUMO DOS GRÁFICOS:
1. 🏃‍♀️ Marina - Densidade nutricional e relação calorias/proteína
2. 💪 Carlos - Eficiência proteica e relação proteína/gordura
3. 👨‍👩‍👧‍👦 Ana - TOP 15 alimentos ricos em cálcio
4. 🩺 Roberto - Melhores opções para diabéticos
5. 📊 Visão Geral - TOP 10 alimentos mais balanceados
🎯 Pronto para relatórios de nutrição personalizada!
""")

