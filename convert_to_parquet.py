"""
convert_to_parquet.py
---------------------
Script para converter o arquivo 'food.csv' para o formato Parquet,
otimizando espaço e desempenho em análises de dados nutricionais.
"""

import pandas as pd
import time
import os
import sys

# ===============================================
# 🔧 CONFIGURAÇÕES
# ===============================================
CSV_FILE = "food.csv"
PARQUET_FILE = "food.parquet"

# ===============================================
# ⚙️ FUNÇÕES AUXILIARES
# ===============================================

def format_size(size_bytes: float) -> str:
    """Formata o tamanho do arquivo em MB."""
    return f"{size_bytes / (1024 * 1024):.2f} MB"

def compare_files(csv_path: str, parquet_path: str) -> None:
    """Compara tamanho e tempo de leitura entre CSV e Parquet."""
    print("\n📊 Comparando desempenho entre formatos...\n")


    csv_size = os.path.getsize(csv_path)
    parquet_size = os.path.getsize(parquet_path)
    reduction = (1 - parquet_size / csv_size) * 100

    print(f"📁 Tamanho CSV: {format_size(csv_size)}")
    print(f"📦 Tamanho Parquet: {format_size(parquet_size)}")
    print(f"💾 Redução: {reduction:.1f}%\n")


    start_csv = time.time()
    pd.read_csv(csv_path)
    csv_time = time.time() - start_csv

    start_parquet = time.time()
    pd.read_parquet(parquet_path)
    parquet_time = time.time() - start_parquet

    print(f"⏱️ Tempo de leitura CSV: {csv_time:.4f} s")
    print(f"⚡ Tempo de leitura Parquet: {parquet_time:.4f} s")


    if parquet_time < csv_time:
        print("\n✅ Parquet mais rápido e mais leve!")
    else:
        print("\nℹ️ CSV mais rápido (dataset pequeno, variação normal).")


# ===============================================
# 🚀 EXECUÇÃO PRINCIPAL
# ===============================================
def main():
    print("🔄 Iniciando conversão CSV → Parquet...\n")


    if not os.path.exists(CSV_FILE):
        print(f"❌ Arquivo '{CSV_FILE}' não encontrado.")
        sys.exit(1)


    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✅ CSV carregado com sucesso! ({len(df):,} registros)\n")


        df.to_parquet(PARQUET_FILE, index=False)
        print(f"🎉 Arquivo salvo como '{PARQUET_FILE}'\n")


        compare_files(CSV_FILE, PARQUET_FILE)


    except Exception as e:
        print(f"❌ Erro durante a conversão: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
