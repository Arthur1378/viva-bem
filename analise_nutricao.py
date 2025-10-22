import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv('food.cv.csv')

# APRESENTANDO OS DADOS (ANÁLISE EXPLORATÓRIA)

# Configurando o estilo dos gráficos
sns.set_style("whitegrid")

# Gráfico 1: Distribuição de Quilocalorias (o novo 'Calories')
plt.figure(figsize=(10, 6))
sns.histplot(df['Data.Kilocalories'], bins=30, kde=True)
plt.title('Distribuição de Quilocalorias nos Alimentos')
plt.xlabel('Quilocalorias')
plt.ylabel('Frequência')
plt.show()

# Gráfico 2: Relação entre Proteína e Gordura Total
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Data.Protein', y='Data.Fat.Total Lipid', data=df, alpha=0.6)
plt.title('Relação entre Proteína e Gordura Total')
plt.xlabel('Proteína (g)')
plt.ylabel('Gordura Total (g)')
plt.show()

# Gráfico 3: Alimentos com mais açúcar (usando a coluna 'Description')
top_10_acucar = df.sort_values(by='Data.Sugar Total', ascending=False).head(10)
plt.figure(figsize=(12, 8))
sns.barplot(x='Data.Sugar Total', y='Description', data=top_10_acucar, palette='viridis')
plt.title('Top 10 Alimentos com Mais Açúcar')
plt.xlabel('Açúcar Total (g)')
plt.ylabel('Alimento (Descrição)')
plt.tight_layout()
plt.show()

##PREPARANDO OS DADOS PARA MACHINE LEARNING

# Lista das colunas com dados nutricionais para o clustering
colunas_nutricionais = [col for col in df.columns if col.startswith('Data.') and 'Household' not in col]

# Selecionar e tratar valores ausentes (uma abordagem simples é preencher com 0)
df_nutricional = df[colunas_nutricionais].fillna(0)

# Normalizar os dados para que todas as colunas tenham a mesma escala
scaler = StandardScaler()
dados_normalizados = scaler.fit_transform(df_nutricional)

## PASSO 4: IDENTIFICANDO PADRÕES COM K-MEANS

# Método do Cotovelo para encontrar o número ideal de clusters (K)
inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(dados_normalizados)
    inertia.append(kmeans.inertia_)

# Plotar o gráfico do cotovelo
plt.figure(figsize=(10, 6))
plt.plot(k_range, inertia, marker='o')
plt.title('Método do Cotovelo (Elbow Method)')
plt.xlabel('Número de Clusters (K)')
plt.ylabel('Inertia')
plt.xticks(k_range)
plt.show()

# Aplicar K-Means com o K ideal (ex: 4, baseado no "cotovelo" do gráfico)
k_ideal = 4
kmeans = KMeans(n_clusters=k_ideal, random_state=42, n_init='auto')
kmeans.fit(dados_normalizados)

# Adicionar os resultados (rótulos dos clusters) de volta ao DataFrame original
df['Cluster'] = kmeans.labels_

##ANALISANDO E INTERPRETANDO OS CLUSTERS

# Calcular a média nutricional para cada grupo/cluster
cluster_analysis = df.groupby('Cluster')[colunas_nutricionais].mean()
print("\n--- Análise Nutricional Média por Cluster ---")
print(cluster_analysis[['Data.Kilocalories', 'Data.Protein', 'Data.Fat.Total Lipid', 'Data.Carbohydrate', 'Data.Sugar Total']])

# Visualizar a separação dos clusters
plt.figure(figsize=(12, 7))
sns.scatterplot(data=df, x='Data.Kilocalories', y='Data.Sugar Total', hue='Cluster', palette='Set1', alpha=0.7)
plt.title('Clusters de Alimentos por Quilocalorias e Açúcar Total')
plt.xlabel('Quilocalorias')
plt.ylabel('Açúcar Total (g)')
plt.legend(title='Cluster')
plt.show()
