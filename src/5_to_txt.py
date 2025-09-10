# csv zu txt
import pandas as pd
import glob
import os

csv_folder = "daten/epochen_csv/"
output_folder = "daten/epochen_txt/"

os.makedirs(output_folder, exist_ok=True)

files = glob.glob(os.path.join(csv_folder, "*.csv"))

for file in files:
    df = pd.read_csv(file, encoding="utf-8")
    if "Übersetzung" in df.columns:
        base_name = os.path.splitext(os.path.basename(file))[0]
        output_file = os.path.join(output_folder, base_name + ".txt")
        
        with open(output_file, "w", encoding="utf-8") as f:
            for text in df["Übersetzung"].dropna():
                f.write(str(text) + "\n")
