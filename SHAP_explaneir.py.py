import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from matplotlib.colors import LinearSegmentedColormap

# Configurações de estilo para matching com a imagem
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'

# Dados de exemplo baseados na imagem
features = [
    'num_ano_construcao',
    'remainder_cluster',
    'num_area_terreno',
    'cat_bairro_BOA VIAGEM',
    'num_area_construida',
    'cat_bairro_VARZEA',
    'cat_bairro_PINA',
    'cat_bairro_IPUTINGA',
    'cat_bairro_IMBIRIBEIRA',
    'cat_bairro_CASA AMARELA',
    'cat_bairro_GRACAS',
    'cat_tipo_imovel_Casa',
    'cat_tipo_imovel_Apartamento',
    'cat_bairro_CORDEIRO',
    'cat_bairro_MADALENA',
    'cat_bairro_TORRE',
    'cat_bairro_CAMPO GRANDE',
    'cat_bairro_SANTO AMARO',
    'cat_bairro_TEJIPIO',
    'cat_bairro_ENCRUZILHADA'
]

# Valores SHAP médios (exemplo)
shap_values = np.array([
    0.35, 0.28, 0.25, 0.22, 0.20, 0.18, 0.16, 0.15, 0.14, 0.13,
    0.12, 0.11, 0.10, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03
])

# Valores das features (normalizados para cor)
feature_values = np.array([
    0.8, 0.6, 0.9, 1.0, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1,
    0.6, 0.8, 0.7, 0.4, 0.3, 0.5, 0.2, 0.1, 0.6, 0.4
])

def create_shap_summary_plot_style(shap_values, features, feature_values, class_name="Econômico"):
    """
    Cria um gráfico SHAP summary plot no estilo da imagem fornecida
    """
    # Ordenar por importância absoluta
    idx_sorted = np.argsort(np.abs(shap_values))[::-1]
    shap_sorted = shap_values[idx_sorted]
    features_sorted = [features[i] for i in idx_sorted]
    values_sorted = feature_values[idx_sorted]
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Configurar cores - gradiente vermelho-azul
    cmap = LinearSegmentedColormap.from_list('rdbu', ['#0000FF', '#FF0000'])
    colors = cmap(values_sorted)
    
    # Criar barras horizontais
    y_pos = np.arange(len(features_sorted))
    bars = ax.barh(y_pos, shap_sorted, color=colors, alpha=0.8, height=0.8)
    
    # Adicionar linha vertical no zero
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
    
    # Configurar eixos
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features_sorted, fontsize=11)
    ax.set_xlabel('SHAP value (impact on model output)', fontsize=12, fontweight='bold')
    ax.set_xlim(-0.4, 0.4)
    
    # Adicionar título
    ax.set_title(f'Impacto das Features na Classe: {class_name}', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Adicionar legenda de cores
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.8, pad=0.02)
    cbar.set_label('Feature value\nHigh          Low', 
                  rotation=0, labelpad=20, fontsize=10, fontweight='bold')
    cbar.ax.yaxis.set_label_position('left')
    
    # Melhorar aparência
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    
    # Adicionar grid
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Inverter eixo Y para ter o mais importante no topo
    ax.invert_yaxis()
    
    plt.tight_layout()
    return fig, ax

# Criar o gráfico principal
fig, ax = create_shap_summary_plot_style(shap_values, features, feature_values, "Econômico")
plt.show()

# Versão alternativa com mais detalhes
def create_detailed_shap_plot(shap_values, features, feature_values, class_name="Econômico"):
    """
    Versão mais detalhada do gráfico SHAP
    """
    # Ordenar por importância
    idx_sorted = np.argsort(np.abs(shap_values))[::-1]
    shap_sorted = shap_values[idx_sorted]
    features_sorted = [features[i] for i in idx_sorted]
    values_sorted = feature_values[idx_sorted]
    
    # Criar figura com subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # Gráfico 1: Barras horizontais (estilo original)
    cmap = LinearSegmentedColormap.from_list('rdbu', ['#0000FF', '#FF0000'])
    colors = cmap(values_sorted)
    
    y_pos = np.arange(len(features_sorted))
    bars = ax1.barh(y_pos, shap_sorted, color=colors, alpha=0.8, height=0.7)
    
    ax1.axvline(x=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(features_sorted, fontsize=10)
    ax1.set_xlabel('SHAP value (impact on model output)', fontsize=11, fontweight='bold')
    ax1.set_xlim(-0.4, 0.4)
    ax1.set_title(f'Impacto das Features - {class_name}', fontsize=13, fontweight='bold')
    ax1.grid(True, axis='x', alpha=0.3, linestyle='--')
    ax1.invert_yaxis()
    
    # Gráfico 2: Beeswarm plot simplificado
    for i, (shap_val, feat_val) in enumerate(zip(shap_sorted, values_sorted)):
        color = cmap(feat_val)
        ax2.scatter(shap_val, i, c=[color], s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
    ax2.set_yticks(range(len(features_sorted)))
    ax2.set_yticklabels(features_sorted, fontsize=10)
    ax2.set_xlabel('SHAP value', fontsize=11, fontweight='bold')
    ax2.set_ylabel('')
    ax2.set_title(f'Distribuição - {class_name}', fontsize=13, fontweight='bold')
    ax2.grid(True, axis='x', alpha=0.3, linestyle='--')
    ax2.set_xlim(-0.4, 0.4)
    
    # Adicionar legenda de cores
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=[ax1, ax2], orientation='vertical', 
                       shrink=0.6, pad=0.05)
    cbar.set_label('Feature Value\nHigh          Low', 
                  rotation=0, labelpad=25, fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    return fig, (ax1, ax2)

# Criar versão detalhada
fig_detailed, axes = create_detailed_shap_plot(shap_values, features, feature_values, "Econômico")
plt.show()

# Versão para múltiplas classes
def create_multi_class_shap_plots(shap_dict, features, feature_values_dict):
    """
    Cria gráficos SHAP para múltiplas classes
    """
    classes = list(shap_dict.keys())
    n_classes = len(classes)
    
    fig, axes = plt.subplots(1, n_classes, figsize=(6*n_classes, 10))
    
    if n_classes == 1:
        axes = [axes]
    
    for idx, (class_name, class_shap) in enumerate(shap_dict.items()):
        ax = axes[idx]
        class_feature_values = feature_values_dict[class_name]
        
        # Ordenar
        idx_sorted = np.argsort(np.abs(class_shap))[::-1]
        shap_sorted = class_shap[idx_sorted]
        features_sorted = [features[i] for i in idx_sorted]
        values_sorted = class_feature_values[idx_sorted]
        
        # Criar gradiente de cores
        cmap = LinearSegmentedColormap.from_list('rdbu', ['#0000FF', '#FF0000'])
        colors = cmap(values_sorted)
        
        # Plot
        y_pos = np.arange(len(features_sorted))
        bars = ax.barh(y_pos, shap_sorted, color=colors, alpha=0.8, height=0.7)
        
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(features_sorted, fontsize=9)
        ax.set_xlabel('SHAP value', fontsize=10, fontweight='bold')
        ax.set_xlim(-0.4, 0.4)
        ax.set_title(f'Classe: {class_name}', fontsize=12, fontweight='bold')
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.invert_yaxis()
    
    plt.tight_layout()
    return fig, axes

# Exemplo para múltiplas classes
shap_multi = {
    "Econômico": np.array([0.35, 0.28, 0.25, 0.22, 0.20, 0.18, 0.16, 0.15, 0.14, 0.13]),
    "Intermediário": np.array([0.25, 0.22, 0.20, 0.18, 0.16, 0.15, 0.14, 0.13, 0.12, 0.11]),
    "Alto Padrão": np.array([0.30, 0.27, 0.24, 0.21, 0.19, 0.17, 0.15, 0.14, 0.13, 0.12])
}

feature_values_multi = {
    "Econômico": np.array([0.8, 0.6, 0.9, 1.0, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1]),
    "Intermediário": np.array([0.7, 0.8, 0.6, 0.5, 0.9, 0.4, 0.3, 0.2, 0.1, 0.5]),
    "Alto Padrão": np.array([0.9, 0.7, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.6])
}

features_short = features[:10]  # Apenas as 10 principais

fig_multi, axes_multi = create_multi_class_shap_plots(shap_multi, features_short, feature_values_multi)
plt.show()

# Função para integrar com modelo real
def plot_shap_from_model(model, X_test, feature_names, class_names=None):
    """
    Gera gráficos SHAP a partir de um modelo treinado
    """
    # Criar explainer
    if hasattr(model, 'estimators_'):
        explainer = shap.TreeExplainer(model)
    else:
        explainer = shap.Explainer(model, X_test)
    
    # Calcular SHAP values
    shap_values = explainer(X_test)
    
    # Se for multi-class, plotar para cada classe
    if len(shap_values.shape) == 3 and class_names is not None:
        n_classes = shap_values.shape[2]
        
        fig, axes = plt.subplots(1, n_classes, figsize=(6*n_classes, 10))
        
        for i in range(n_classes):
            class_name = class_names[i] if class_names else f"Classe {i}"
            
            # Calcular valores médios
            mean_shap = np.mean(shap_values.values[:, :, i], axis=0)
            mean_feature_values = np.mean(X_test, axis=0)
            
            # Ordenar
            idx_sorted = np.argsort(np.abs(mean_shap))[::-1][:15]  # Top 15
            shap_sorted = mean_shap[idx_sorted]
            features_sorted = [feature_names[j] for j in idx_sorted]
            values_sorted = mean_feature_values[idx_sorted]
            
            # Normalizar valores para cor
            values_normalized = (values_sorted - np.min(values_sorted)) / (np.max(values_sorted) - np.min(values_sorted))
            
            # Plot
            cmap = LinearSegmentedColormap.from_list('rdbu', ['#0000FF', '#FF0000'])
            colors = cmap(values_normalized)
            
            y_pos = np.arange(len(features_sorted))
            bars = axes[i].barh(y_pos, shap_sorted, color=colors, alpha=0.8, height=0.7)
            
            axes[i].axvline(x=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
            axes[i].set_yticks(y_pos)
            axes[i].set_yticklabels(features_sorted, fontsize=9)
            axes[i].set_xlabel('SHAP value', fontsize=10)
            axes[i].set_title(f'Impacto - {class_name}', fontsize=12, fontweight='bold')
            axes[i].grid(True, axis='x', alpha=0.3)
            axes[i].invert_yaxis()
        
        plt.tight_layout()
        
    else:
        # Para binary classification
        mean_shap = np.mean(np.abs(shap_values.values), axis=0)
        idx_sorted = np.argsort(mean_shap)[::-1][:15]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Usar a função anterior
        create_shap_summary_plot_style(
            mean_shap[idx_sorted], 
            [feature_names[i] for i in idx_sorted],
            np.ones(len(idx_sorted)),  # Valores dummy
            "Target"
        )
    
    return fig

print("✅ Todos os gráficos SHAP no estilo solicitado foram criados!")
print("\n🎨 Características dos gráficos:")
print("   • Barras horizontais coloridas")
print("   • Gradiente azul (Low) → vermelho (High)")
print("   • Linha vertical no zero")
print("   • Features ordenadas por importância")
print("   • Legenda de Feature Value")
print("   • Grid para melhor leitura")