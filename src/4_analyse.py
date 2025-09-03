import nltk
import pandas as pd
from pandas import Series
import matplotlib
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud

nltk.download('punkt')
nltk.download('stopwords')

# CSV laden
#df = pd.read_csv("data/extrahierte_daten_bereinigt2.csv")
#df = pd.read_csv("epoche_csv/Dritte_Zwischenzeit.csv", encoding='utf-8')
#df = pd.read_csv("epoche_csv/Zweite_Zwischenzeit.csv", encoding='utf-8')
#df = pd.read_csv("epoche_csv/Mittleres_Reich.csv", encoding='utf-8')
#df = pd.read_csv("epoche_csv/Neues_Reich.csv", encoding='utf-8')
#df = pd.read_csv("epoche_csv/Altes_Reich.csv", encoding='utf-8')
df = pd.read_csv("epochen_csv\Spätzeit.csv", encoding='utf-8')
#df = pd.read_csv("epoche_csv/Griechisch-römische_Zeit.csv", encoding='utf-8')



stop = set(stopwords.words('german'))

#!!!! Mit Lemma ersetzen!
stemmer = SnowballStemmer("german")

text_raw = df['Übersetzung'].str.cat(sep=' ').lower().replace('-', ' ')

tokens = nltk.word_tokenize(text_raw, language='german')

tokens = [stemmer.stem(w) for w in tokens if w not in stop and w.isalpha()]

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

print("Konkordanz für 'isis':")
try:
    text.concordance("isis")
except Exception as e:
    print("Fehler bei concordance:", e)

print("Ähnliche Wörter zu 'isis':")
text.similar("isis")

print("Dispersionsdiagramm:")
text.dispersion_plot(["isis", "osiris"])

print("Kollokationen:")
text.collocations()

# Lexikalische Vielfalt
lexical_diversity = unique_words_count / len(tokens)
print("Lexikalische Vielfalt:", lexical_diversity)

# Series-Analyse
wordSeries = Series(tokens)
wordCounts = wordSeries.value_counts()
print("Häufigste Wörter in Series:")
print(wordCounts.head(10))

# Optional: Anzahl bestimmter Wörter
if 'pharao' in wordCounts:
    isisNum = wordCounts['pharao']
    print("Anzahl 'pharao':", isisNum)

# WordCloud
font_path = matplotlib.font_manager.findfont("DejaVu Sans")

words = " ".join(tokens)
wordcloud = WordCloud(background_color="white", width=800, height=400).generate(words)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.show()
