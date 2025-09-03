# https://www.datacamp.com/tutorial/what-is-topic-modeling

# Leider sind die Ergebnisse hier nicht sonderlich aussagekräftig

from nltk.corpus import stopwords
import string


import spacy

nlp = spacy.load("de_core_news_lg", disable=["parser", "ner", "textcat"])

dateipfade = [
    "uebersetzungen_export/Dritte_Zwischenzeit.txt",
    "uebersetzungen_export/Zweite_Zwischenzeit.txt",
    "uebersetzungen_export/Mittleres_Reich.txt",
    "uebersetzungen_export/Neues_Reich.txt",
    "uebersetzungen_export/Spätzeit.txt",
    "uebersetzungen_export/Griechisch-römische_Zeit.txt",
]


docs = {}
for p in dateipfade:
    with open(p, "r", encoding="utf-8") as f:
        docs[p] = f.read()

corpus = list(docs.values())


stop = set(stopwords.words("german"))
exclude = set(string.punctuation)

def clean(doc: str) -> str:

    stop_free = " ".join([w for w in doc.lower().split() if w not in stop])
    stop_free.replace("-", " ")
    # ggf rausmachen
    punc_free = "".join(ch for ch in stop_free if ch not in exclude)
   
    spacy_doc = nlp(punc_free)
    lemmas = [t.lemma_ for t in spacy_doc if t.lemma_ and t.lemma_ != " "]
    normalized = " ".join(lemmas)
    return normalized

clean_corpus = [clean(doc).split() for doc in corpus]

print("Erste 10 Wörter im bereinigten Korpus:", clean_corpus[0][:10])

from gensim import corpora
dictionary = corpora.Dictionary(clean_corpus)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_corpus]

from gensim.models import LsiModel
lsa = LsiModel(doc_term_matrix, num_topics=6, id2word = dictionary) # Topicanzahl
print(lsa.print_topics(num_topics=6, num_words=5))

print("------------------------------------------------------------")
from gensim.models import LdaModel
lda = LdaModel(doc_term_matrix, num_topics=6, id2word = dictionary)
print(lda.print_topics(num_topics=6, num_words=3))



