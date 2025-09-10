#Viz für einzelne Orte anhand von Jahreszahlen/Dynastien

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_deir_el_medineh(input_path="data/extrahierte_daten_bereinigt.csv"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Datei nicht gefunden: {input_path}")

    df = pd.read_csv(input_path, encoding="utf-8")

    df_deir = df[df['Herkunft'] == "Deir el-Medineh"]

    if df_deir.empty:
        print("Keine Einträge für 'Deir el-Medineh' gefunden.")
        return

    counts = df_deir['Datierung'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(counts.index, counts.values)
    ax.set_xlabel("Datierung")
    ax.set_ylabel("Anzahl")
    ax.set_title("Funde in Deir el-Medineh nach Datierung")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_deir_el_medineh()
