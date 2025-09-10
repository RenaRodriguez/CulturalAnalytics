# TF-IDF Ergebnisse in Tabellen 

import glob
import pandas as pd
from pathlib import Path

path = r'epochen_txt/tf_idf_output'
all_files = sorted(glob.glob(path + "/*.csv"))

li = []
for filename in all_files:
    df = pd.read_csv(filename, header=0, usecols=[1], nrows=15, encoding="utf-8-sig")
    li.append(df)

frame = pd.concat(li, axis=1, ignore_index=True)

column_names = [Path(f).stem for f in all_files]

frame.columns = column_names

frame.to_csv('epochen_txt/tf_idf_output/tf_idf_table.csv', sep=',', index=False, encoding="utf-8-sig")
