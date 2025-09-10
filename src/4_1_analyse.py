# Textanalyse mit NLTK, Dispersion-Plot nach TF-IDF und Wordclouds

import nltk
import pandas as pd
from pandas import Series
import matplotlib
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud
import spacy
import seaborn as sns



nltk.download('punkt')
nltk.download('stopwords')

# CSV laden
df = pd.read_csv("daten\epochen_csv\gesamt_clean.csv", encoding='utf-8')
#df = pd.read_csv("daten\epochen_csv/Dritte_Zwischenzeit.csv", encoding='utf-8')
#df = pd.read_csv("daten\epochen_csv/Zweite_Zwischenzeit_clean.csv", encoding='utf-8')
#df = pd.read_csv("daten\epochen_csv\Mittleres_Reich_clean.csv", encoding='utf-8')
#df = pd.read_csv(r"daten\epochen_csv\Neues_Reich_clean.csv", encoding='utf-8')
#df = pd.read_csv("daten\epoche_csv/Altes_Reich.csv", encoding='utf-8')
#df = pd.read_csv("daten\epochen_csv\Spätzeit_clean.csv", encoding='utf-8')
#df = pd.read_csv("daten\epochen_csv/Griechisch-römische_Zeit_clean.csv", encoding='utf-8')


# Sortieren für den Dispersion-Plot
epochen_order = [
    "Mittleres Reich",
    "Zweite Zwischenzeit",
    "Neues Reich",
    "Dritte Zwischenzeit",
    "Spätzeit",
    "Griechisch-römische Zeit"
]

if "Epoche" in df.columns:
    df["Epoche"] = pd.Categorical(df["Epoche"], categories=epochen_order, ordered=True)
    df = df.sort_values("Epoche")


stop = set(stopwords.words('german'))
stopwords_zusätzlich = [
    "wörtl", "dh","--", "oä" ]

#spacy lemma
nlp = spacy.load("de_core_news_lg")
nlp.max_length = 2_000_000  # für die größere Modelle, geht zeittechnisch noch total
# bisschen doof, dass einige Namen vom Lemmazizer überschrieben werden
lemma_exceptions = [
    "setne", "tamounis", "osiris", "pami", "naneferkaptha", "inaros", "anchhor",
    "siosiris", "imen", "niut", "landmann", "jenseits", "oberdomänenvorsteher", "lhg",
    "bata", "ba", "teodjoi", "merire", "peteese", "senti", "irtutu", "horudja", "chons",
    "schiffsmeister", "ubainer", "kartusche", "bata"
]

text_raw = df["Übersetzung"].fillna("").str.cat(sep=" ").replace("-", " ")

doc = nlp(text_raw) # tokenisierung über spaCy statt nltk
tokens = [
    token.text.lower() if token.text.lower() in lemma_exceptions
    else token.lemma_.lower()
    for token in doc
    if token.is_alpha and token.pos_ in ["NOUN", "ADJ"] # das hier könnte auch noch Verben beinhalten
]

tokens = [
    token for token in tokens
    if token not in nlp.Defaults.stop_words and token not in stopwords_zusätzlich
]

print("Erste 10 gestemmte Wörter:", tokens[:10])

# Häufigkeitsverteilung
word_freq = nltk.FreqDist(tokens)
print("Anzahl der Wörter:", len(tokens))

print("Häufigste Wörter:")
for word, freq in word_freq.most_common(10):
    print(f"{word}: {freq}")

unique_words = set(tokens)
unique_words_count = len(unique_words)
print("Anzahl einzigartiger Wörter:", unique_words_count)

sortedWords = sorted(word_freq, key=word_freq.get, reverse=True)
print("Erste 10 einzigartige Wörter:", sortedWords[:10])

# Textanalyse mit NLTK
text = nltk.Text(tokens)

print("Konkordanz für 'gott':")
try:
    text.concordance("gott")
except Exception as e:
    print("Fehler bei concordance:", e)

print("Ähnliche Wörter zu 'gott':")
text.similar("gott")

print("Dispersionsdiagramm:")
# anhand der TF-IDF Ergebnisse, leider aussagelos
text.dispersion_plot(["gott", 
                      # Mittleres Reich
                      "Mittleres Reich", "landmann", "ba", "insel", "jenseits", "anlegestelle", 
                      # Zweite Zwischenzeit
                      "Zweite Zwischenzeit", "ubainer","norm","vorlesepriester","wachs","hausmeister",
                      # Neues Reich
                      "Neues Reich", "tanne","pharao","götterneunheit","nahrung",
                      # Dritte Zwischenzeit
                      "Dritte Zwischenzeit", "amun","amunrasonther","götterbarke","tamounis","auge",
                      # Spätzeit
                      "Spätzeit", "chons","merire","peteese","irturu","senti",
                      # Griechisch-römische Zeit
                      "Griechisch-römische Zeit", "pami","isis","osiris","inaro","siosire",
                   ])

print("Kollokationen:")
kollokationen = text.collocations()
print(kollokationen)


# Lexikalische Vielfalt -> wsl nicht so wichtig, bei Übersetzungen von einer Person
#lexical_diversity = unique_words_count / len(tokens)
#print("Lexikalische Vielfalt:", lexical_diversity)

# Series-Analyse
# wird u.a. auch für die Balkendiagramme genutzt
wordSeries = Series(tokens)
wordCounts = wordSeries.value_counts()
print("Häufigste Wörter in Series:")
print(wordCounts.head(10))

# Optional: Anzahl bestimmter Wörter
#if 'pharao' in wordCounts:
#    isisNum = wordCounts['pharao']
#    print("Anzahl 'pharao':", isisNum)

# WordCloud
font_path = matplotlib.font_manager.findfont("DejaVu Sans")

words = " ".join(tokens)
wordcloud = WordCloud(background_color="white", width=800, height=400).generate(words)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.show()

# Wort-Häufigkeits-Balkendiagramm
top_n = 10
freq_df = wordCounts.head(top_n).reset_index()
freq_df.columns = ["Wort", "Frequenz"]

plt.figure(figsize=(10, 6))
sns.barplot(x="Frequenz", y="Wort", data=freq_df, palette="viridis")
plt.title("Häufigste Wörter", fontsize=14)
plt.xlabel("Anzahl")
plt.ylabel("Wort")
plt.tight_layout()
plt.show()




