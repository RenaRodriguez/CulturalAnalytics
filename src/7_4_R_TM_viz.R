#Viz der Ergebnisse aus dem R TM


options(stringsAsFactors = FALSE)
require(quanteda)
require(topicmodels)
require(lda)
require(htmltools)
require(ggplot2)
require(reshape2)

load("DTM.RData")
load("tmResult.RData")
load("topicModel.RData")
load("corpus.RData")
load("text_data.RData")
K <- topicModel@k 


theta <- tmResult$topics
phi <- tmResult$terms


# word cloud
library(wordcloud2)

top5termsPerTopicProb <- lda::top.topic.words(phi, 5, by.score = T)
topicNames <- apply(top5termsPerTopicProb, 2, paste, collapse = " ")

topicToViz <- 11 # hier ändern
topicToViz <- grep('sonnenscheibe', topicNames)[1] #oder hier
# 40 terme
top40terms <- sort(phi[topicToViz,], decreasing = TRUE)[1:40]
words <- names(top40terms)
# wslkeit
probabilities <- sort(phi[topicToViz,], decreasing = TRUE)[1:40]
wordcloud2(data.frame(words, probabilities))


install.packages("pals")
library(pals)

topicProportions <- colSums(theta) / sum(theta)
names(topicProportions) <- topicNames

topicProportions <- topicProportions[order(topicProportions)]

topicsOrd <- factor(
  names(topicProportions), 
  levels = names(topicProportions), 
  ordered = T) 


colorScale <- rainbow(length(topicsOrd))

refOrdColors <- data.frame(topicsOrd, colorScale)

topicProportions_df <- melt(topicProportions) 

topicProportions_df$topicNamesFactor <- refOrdColors$topicsOrd 

bp <- ggplot(topicProportions_df, aes(x = "", y = value, fill = refOrdColors$topicsOrd)) + 
  geom_bar(width = 1, stat = "identity") +
  scale_fill_manual(values = refOrdColors$colorScale) 

require(scales)
pie <- bp + coord_polar("y", start = 0) + theme_minimal() + 
  theme(
    axis.text.x = element_blank(), 
    axis.title.x = element_blank(), 
    axis.title.y = element_blank(),
    panel.border = element_blank(),
    panel.grid = element_blank(),
    axis.ticks = element_blank(),
    legend.position = "left", 
    legend.key.width = unit(3, "mm"),
    legend.key.height = unit(3, "mm"),
    plot.title = element_text(size = 14, face = "bold")
  ) +
  ggtitle("Topic distribution in corpus") +
  geom_text(size = 3, aes(x = 1.7, 
                          label = percent(value)), 
            position = position_stack(vjust = 0.5)) + 
  guides(fill = guide_legend(title = "Topic names", reverse = T))
print(pie)

# balkendiagramm
ggplot(data = topicProportions_df, 
       aes(x = topicNamesFactor, y = value, fill = refOrdColors$topicsOrd)) + # set data for axis and fill a gradient
  geom_bar(stat = "identity", width = .5) +
  scale_fill_manual(values = refOrdColors$colorScale) +  
  coord_flip() +
  guides(fill = FALSE) +
  ggtitle("Topic proportions") +
  xlab("Topic name") + 
  ylab("Proportion") 


#--------------------------------------------------------------------
install.packages("LDAvis")
require(LDAvis)

dtm_topicmodels <- convert(DTM, to = "topicmodels")

doc.length     <- slam::row_sums(dtm_topicmodels)
term.frequency <- slam::col_sums(dtm_topicmodels)
vocab          <- colnames(dtm_topicmodels)
vocab          <- enc2utf8(vocab)  # Umlaut-/Sonderzeichen-sicher für HTML/JS

json <- createJSON(
  phi   = phi, 
  theta = theta, 
  doc.length = as.numeric(doc.length), 
  vocab = vocab, 
  term.frequency = as.numeric(term.frequency)
)

# Visualisieren
tmpdir <- tempfile("ldavis_"); dir.create(tmpdir)
serVis(json, out.dir = tmpdir, open.browser = interactive())  # öffnet Browser, wenn interaktiv

