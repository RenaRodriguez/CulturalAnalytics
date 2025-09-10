# Beste was wir haben, immer noch nicht gut :')

# !!!! Dieser Code liefert NICHT die gewünschten Ergebnisse. Nicht benutzen !!!!


import os
import numpy as np
import spacy
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis


nlp = spacy.load("de_core_news_lg")
#nlp = spacy.load("de_core_news_md")
#nlp = spacy.load("de_core_news_sm")
nlp.max_length = 2_000_000  # für die größere Modelle, geht zeittechnisch noch total


text_path = "epochen_txt"  
texts = []
titles = []

for root, dirs, files in os.walk(text_path):
    for filename in files:
        if filename.endswith(".txt"):
            full_path = os.path.join(root, filename)
            with open(full_path, 'r', encoding='utf-8') as rf:
                texts.append(rf.read().lower())
                titles.append(filename[:-4].lower())

if not texts:
    print("Keine Textdatein im angegebenen Ordner gefunden.")
    exit()

# nlp fun ab hier
refined_texts = []

stopwords_zusätzlich = [
    "Wörtl", "dh","--", "oä" ]

for text in texts:
    doc = nlp(text) # tokenisierung über spaCy statt nltk
    tokens = [token.lemma_ for token in doc if token.is_alpha and token.pos_ in ["NOUN", "ADJ"]] # Lemmatisierung --> nur Nomen und Adjektive, weil die Ergebnisse schwammig waren bis jetzt 
    tokens = [token for token in tokens if token not in nlp.Defaults.stop_words and token not in stopwords_zusätzlich] # Stopwörter entfernen gesondert
    refined_texts.append(tokens)

#Dictionary und BoW
dictionary = corpora.Dictionary(refined_texts)
corpus = [dictionary.doc2bow(text) for text in refined_texts]

if not any(len(doc) > 0 for doc in corpus):
    print("Corpus ist leer. Dictionary und BoW prüfen")
    exit()

# LDA-Modell 
num_topics = 6  
#10
# 9 2 große, 2 kleine 
# 8 2 große, ein kleines  
# 7 2 große, ein kleines  
# 6 3 große 1 kleines
# 5 2 große, ein kleines
# 4 wie 5
# 3 2 große                                                               

# !!!! Hier Anzahl anpassen !!!!
lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=num_topics,
    random_state=42,
    passes=250,
    alpha=0.01,
    per_word_topics=True,
)


print("Themenübersicht:")
topics = lda_model.show_topics(num_topics=num_topics, num_words=10, formatted=True)
for topic in topics:
    print(topic)

vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(vis_data, 'lda_visualisierung.html')
print("Datei erstellt.")
