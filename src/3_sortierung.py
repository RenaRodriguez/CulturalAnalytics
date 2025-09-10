# Aufteilung in txt und csv nach Epochen

import pandas as pd
import os
import re
import matplotlib.pyplot as plt

df = pd.read_csv("daten/extrahierte_daten_bereinigt.csv")
df.sort_values(["Epoche"], axis=0, ascending=[True], inplace=True)

gruppen = df.groupby("Epoche")

ausgabeordner_txt = "uebersetzungen_export"
ausgabeordner_csv = "daten/epochen_csv"

def dateiname(text):
    text = text.strip().replace(" ", "_")
    return re.sub(r"[\\/:\*\?\"<>\|]", "_", text)

os.makedirs(ausgabeordner_txt, exist_ok=True)
os.makedirs(ausgabeordner_csv, exist_ok=True)

for epoche, gruppe in gruppen:
    if pd.isna(epoche):
        continue

    uebersetzungen = gruppe["Übersetzung"].dropna()
    if not uebersetzungen.empty:
        dateiname_txt = dateiname(epoche) + ".txt"
        dateipfad_txt = os.path.join(ausgabeordner_txt, dateiname_txt)
        with open(dateipfad_txt, "w", encoding="utf-8") as f:
            for zeile in uebersetzungen:
                f.write(zeile.strip() + "\n")
        print(f"{len(uebersetzungen)} Übersetzungen gespeichert in: {dateipfad_txt}")

    # gesamtt CSV
    dateiname_csv = dateiname(epoche) + ".csv"
    dateipfad_csv = os.path.join(ausgabeordner_csv, dateiname_csv)
    gruppe.to_csv(dateipfad_csv, index=False, encoding="utf-8")
    print(f"{len(gruppe)} gespeichert in: {dateipfad_csv}")

