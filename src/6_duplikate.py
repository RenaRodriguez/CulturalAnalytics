# im endeffekt wurde das manuelle doch zu anstrengend

import pandas as pd

input_file = "daten/extrahierte_daten_bereinigt.csv"
output_file = "daten/epochen_csv/gesamt_clean.csv"

df = pd.read_csv(input_file)
df_clean = df.drop_duplicates(subset=["Datei", "Übersetzung"])
df_clean.to_csv(output_file, index=False)

