# TF-IDF
# Funfact: ich habe genau diesen Code abgegeben für Methods & Application for DH , wo Sie unser OCR Projekt betreut hatten :D

from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


all_txt_files =[]
for file in Path("data/epochen_txt").rglob("*.txt"):
     all_txt_files.append(file.parent / file.name)
# Länge der Liste
n_files = len(all_txt_files)

all_txt_files.sort()
print(all_txt_files[0])

all_docs = []
for txt_file in all_txt_files:
    with open(txt_file, encoding= "utf-8") as f:
        txt_file_as_string = f.read()
    all_docs.append(txt_file_as_string)

vectorizer = TfidfVectorizer(max_df=.65, min_df=1, stop_words=None, use_idf=True, norm=None)
transformed_documents = vectorizer.fit_transform(all_docs)
transformed_documents_as_array = transformed_documents.toarray()
# Länge der Liste verifizieren
print(len(transformed_documents_as_array))

output_filenames = [
    Path("data/epochen_txt/tf_idf_output") / (txt_file.name.replace(".txt", ".csv"))
    for txt_file in all_txt_files
]

# Schleife über die Dokumente
for counter, doc in enumerate(transformed_documents_as_array):
    print(counter)
    tf_idf_tuples = list(zip(vectorizer.get_feature_names_out(), doc))
    one_doc_as_df = pd.DataFrame.from_records(tf_idf_tuples, columns=['term', 'score']).sort_values(by='score', ascending=False).reset_index(drop=True)
    one_doc_as_df.to_csv(output_filenames[counter], encoding="utf-8-sig")
print(one_doc_as_df)