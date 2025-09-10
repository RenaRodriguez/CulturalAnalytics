# Säulendiagramm mit Orten und Epochen

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/extrahierte_daten_bereinigt.csv")

grouped = df.groupby(["Epoche", "Herkunft"]).size().reset_index(name="Anzahl")


pivot = grouped.pivot(index="Herkunft", columns="Epoche", values="Anzahl").fillna(0)

epochen_sorted = [
    "Mittleres Reich",
    "Zweite Zwischenzeit",
    "Neues Reich",
    "Dritte Zwischenzeit",
    "Spätzeit",
    "Griechisch-römische Zeit",
    "Unbekannt"
]

pivot = pivot[epochen_sorted]

pivot["gesamt"] = pivot.sum(axis=1)
pivot = pivot.sort_values("gesamt", ascending=False)
pivot = pivot.drop(columns=["gesamt"])

pivot.plot(kind="bar", stacked=True, figsize=(14, 7))
plt.ylabel("Anzahl")
plt.title("Epoche pro Herkunftsort")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.legend(title="Epoche")
plt.show()