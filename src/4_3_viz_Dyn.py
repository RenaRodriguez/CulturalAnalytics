# Säulendiagramm mit Orten und Jahreszahlen/Dynastien


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/extrahierte_daten_bereinigt.csv")

grouped = df.groupby(["Datierung", "Herkunft"]).size().reset_index(name="Anzahl")


pivot = grouped.pivot(index="Herkunft", columns="Datierung", values="Anzahl").fillna(0)


pivot["gesamt"] = pivot.sum(axis=1)
pivot = pivot.sort_values("gesamt", ascending=False)
pivot = pivot.drop(columns=["gesamt"])

ax = pivot.plot(kind="bar", stacked=True, figsize=(14, 7))
plt.ylabel("Anzahl")
plt.title("Datierung pro Herkunftsort")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()


# muss trotzdem noch manuell angepasst werden
plt.legend(
    title="Datierung",
    fontsize="x-small",       
    title_fontsize="x-small"   
)

plt.show()