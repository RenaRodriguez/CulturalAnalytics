options(stringsAsFactors = FALSE)

library(quanteda)
library(magrittr)
library(dplyr)
library(topicmodels)
library(lda)
library(udpipe)
library(data.table)
library(quanteda.textstats)

german_stopwords <- stopwords("de")

text_data <- read.csv("D:/Code/CA/data/texte.csv", encoding = "UTF-8")
colnames(text_data)
text_data %<>% mutate(d_id = 1:nrow(text_data))


ud_model <- udpipe_download_model(language = "german")
ud_model <- udpipe_load_model(ud_model$file_model)

# POS-Tagging und Lemmatisierung
anno <- udpipe_annotate(ud_model, x = text_data$Übersetzung)
anno_df <- as.data.frame(anno)

#  Nur bestimmte POS behalten (z. B. Nomen, Verben, Adjektive)
anno_df <- anno_df[anno_df$upos %in% c("NOUN", "VERB", "ADJ"), ]

# Gruppiere Lemmata nach Dokument (doc_id)
token_lists <- split(anno_df$lemma, anno_df$doc_id)
token_lists <- lapply(token_lists, function(x) x[!is.na(x) & x != ""])

# Corpus-Objekt 
names(token_lists) <- unique(anno_df$doc_id)
tokens_clean <- as.tokens(token_lists)

tokens_clean <- tokens_remove(tokens_clean, pattern = german_stopwords, padding = TRUE)

# Collocations 
collocations <- textstat_collocations(tokens_clean, min_count = 20) #verändert
collocations <- collocations[1:min(250, nrow(collocations)), ]
collocations <- subset(collocations, lambda > 0)   # höhere Assoziationsstärke
collocations <- head(collocations, 150)
tokens_compounded <- tokens_compound(tokens_clean, collocations)


# Document-Term-Matrix n
DTM <- tokens_compounded %>%
  tokens_remove("") %>%
  dfm() %>%
  dfm_trim(min_docfreq = 10) # erhöht um seltere Terme zu streichen

# LDA
K <- 5
topicModel <- LDA(convert(DTM, to = "topicmodels"), K, method = "Gibbs", control = list(iter = 500, verbose = 20, alpha = 0.5, estimate.beta = TRUE))
tmResult <- posterior(topicModel)
theta <- tmResult$topics

p_w <- colSums(DTM) / sum(DTM)
scoreByLambda <- function(p_w_t, num.words = 10, p_w, lambda) {
  apply(p_w_t, 1, function(x, num.words, p_w, lambda) {
    x <- lambda * log(x) + (1 - lambda) * log(x / p_w)
    return(names(sort(x, decreasing = T)[1:num.words]))
  }, num.words, p_w, lambda)
}
top5termsPerTopicScoreII <- scoreByLambda(tmResult$terms, num.words = 7, p_w, lambda = 0.6)
topicNamesByScoreII <- apply(top5termsPerTopicScoreII, 2, paste, collapse = " ")
topicProportions <- colSums(theta) / sum(theta)
names(topicProportions) <- topicNamesByScoreII

# Dokument-Zuordnung
countsOfPrimaryTopics <- rep(0, K)
names(countsOfPrimaryTopics) <- topicNamesByScoreII
for (i in 1:dim(theta)[1]) {
  topicsPerDoc <- theta[i, ]
  primaryTopic <- order(topicsPerDoc, decreasing = TRUE)[1]
  countsOfPrimaryTopics[primaryTopic] <- countsOfPrimaryTopics[primaryTopic] + 1
}

# Ergebnis
sortByProportion <- sort(topicProportions, decreasing = TRUE)
dfTopicProp <- data.frame(topic = names(sortByProportion), proportion = sortByProportion, row.names = NULL)
sortByPrime <- sort(countsOfPrimaryTopics, decreasing = TRUE)
dfTopicSort <- cbind(dfTopicProp, data.frame(topic2 = names(sortByPrime), count = sortByPrime, row.names = NULL))
View(dfTopicSort)


save(DTM, file = "DTM.RData")
save(text_data, file = "text_data.RData")
save(tokens_clean, file = "corpus.RData")
save(collocations, file = "collocations.RData")
save(topicModel, file = "topicModel.RData")
save(tmResult, file = "tmResult.RData")
save(theta, file = "theta.RData")
