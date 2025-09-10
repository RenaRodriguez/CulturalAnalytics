# !!!! Dieser Code liefert NICHT die gewünschten Ergebnisse. Nicht benutzen !!!!

import numpy as np
import gensim
#!!! dieser Code funltioniert nicht mit den neueren Envoriment!!!
from gensim.models.wrappers import LdaMallet
import spacy
import nltk
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import os   
import nltk
# vis
import pyLDAvis
import pyLDAvis.gensim

texts = []
titles = []
for root, dirs, files in os.walk("daten/epochen_txt"):
    for filename in files:
        with open(os.path.join(root, filename), 'r', encoding='utf-8-sig') as rf:
            texts.append(rf.read().lower())
            titles.append(filename[:-4].lower())

lemmatizer = nltk.WordNetLemmatizer()
stopwords = set(nltk.corpus.stopwords.words('german'))

refinedTexts = []
for text in texts:
    tokenized = nltk.word_tokenize(text)
    #print(tokenized)
    refinedV = [lemmatizer.lemmatize(word, pos = "v",) for word in tokenized if word.isalnum() and word not in stopwords]
    refined = [lemmatizer.lemmatize(word,) for word in refinedV]
    refinedTexts.append(refined)

# Dictionary
corpusDictionary = gensim.corpora.Dictionary(refinedTexts)
print(corpusDictionary)
# Tuple
processedCorpus = [corpusDictionary.doc2bow(text) for text in refinedTexts]

numberOfTopics = 10
os.environ.update({'MALLET_HOME':r'C:/mallet-2.0.8/'})
malletPath = 'C:/mallet-2.0.8/bin/mallet' 


# Model trainieren:
ldaMalletModel = LdaMallet(mallet_path=malletPath, corpus=processedCorpus,
                           id2word=corpusDictionary, num_topics=numberOfTopics,
                           optimize_interval=100, prefix="test")

ldaModel = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(ldaMalletModel)

corpusLda = ldaModel[processedCorpus]

topics = ldaModel.show_topics(num_topics=10, num_words=10)

for topic in topics:
  print(topic)
