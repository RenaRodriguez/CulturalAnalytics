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
K <- topicModel@k # set a global topic model K parameter to use

# From the posterior get theta (p(z|d)) and phi (p(w|z)) 
theta <- tmResult$topics
phi <- tmResult$terms


# visualize topics as word cloud
library(wordcloud2)

#generate the names again to filter for a certain topic
#terms: Function to extract the most likely terms for each topic or the most likely topics for each document.
top5termsPerTopicProb <- lda::top.topic.words(phi, 5, by.score = T)
topicNames <- apply(top5termsPerTopicProb, 2, paste, collapse = " ")

topicToViz <- 11 # change for your own topic of interest
topicToViz <- grep('sonnenscheibe', topicNames)[1] # Or select a topic by a term contained in its name
# select to 40 most probable terms from the topic by sorting the term-topic-probability vector in decreasing order
top40terms <- sort(phi[topicToViz,], decreasing = TRUE)[1:40]
words <- names(top40terms)
# extract the probabilities of each of the 40 terms
probabilities <- sort(phi[topicToViz,], decreasing = TRUE)[1:40]
wordcloud2(data.frame(words, probabilities))







install.packages("pals")
library(pals)

# Again we use the topic distribution over documents to determine the share of each topic
# What are the most probable topics in the entire collection?
topicProportions <- colSums(theta) / sum(theta)
names(topicProportions) <- topicNames

# For the next examples we create a main sorting and coloring of the topics which we could apply to all visualizations in ggplot

# We start with sorting the topics by their probability
topicProportions <- topicProportions[order(topicProportions)]

# ordering in the ggplot library can be done using a factor for the topic labels
topicsOrd <- factor(
  names(topicProportions), # Take the names of the topics as examples
  levels = names(topicProportions), # Set them also as possible levels of the nominal factor
  ordered = T) # the given order of the topic names is also the order of the factor

# next we randomly create some colors from the "rainbow"-palette of R
# colorScale <- sample(rainbow(length(topicsOrd)))
# Alternative: use precompiled color palettes from the the pals package
colorScale <- rainbow(length(topicsOrd))

# Finally, a data frame is created associating the colors with the topic names
refOrdColors <- data.frame(topicsOrd, colorScale)

# ggplot2 does only understand data.frame objects
# melt creates a data.frame from our matrix representing each cell as a row
topicProportions_df <- melt(topicProportions) 

# add the just created factor as name description column to the rows of the data.frame
topicProportions_df$topicNamesFactor <- refOrdColors$topicsOrd 

# Create a bar plot:
# Initialize the plot by assigning the values to the y-axis. The running order of the topics is given by fill and the ordered topic factor. The scale_fill_manual command defines the order of the colors and is assigned to our reference colors.
bp <- ggplot(topicProportions_df, aes(x = "", y = value, fill = refOrdColors$topicsOrd)) + 
  geom_bar(width = 1, stat = "identity") +
  scale_fill_manual(values = refOrdColors$colorScale) 

require(scales)
# from the bar plot create a polar coordinate view, choose a minimal theme
pie <- bp + coord_polar("y", start = 0) + theme_minimal() + 
  theme(
    axis.text.x = element_blank(), 
    axis.title.x = element_blank(), # make every graphical element blank except the pie
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

# balkendiagrammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
ggplot(data = topicProportions_df, 
       aes(x = topicNamesFactor, y = value, fill = refOrdColors$topicsOrd)) + # set data for axis and fill a gradient
  geom_bar(stat = "identity", width = .5) + # define attributes for bars
  scale_fill_manual(values = refOrdColors$colorScale) +  
  coord_flip() + # flip the plot to horizontal bars
  guides(fill = FALSE) + # hide guide
  ggtitle("Topic proportions") + # set the title
  xlab("Topic name") + # set the x axis label
  ylab("Proportion") # set the y axis label


#--------------------------------------------------------------------
install.packages("LDAvis")
require(LDAvis)

# Nutze die gleiche DTM-Form wie im LDA-Call
dtm_topicmodels <- convert(DTM, to = "topicmodels")

# Konsistente Inputs
doc.length     <- slam::row_sums(dtm_topicmodels)
term.frequency <- slam::col_sums(dtm_topicmodels)
vocab          <- colnames(dtm_topicmodels)
vocab          <- enc2utf8(vocab)  # Umlaut-/Sonderzeichen-sicher für HTML/JS

# JSON für LDAvis bauen (ACHTUNG: schließende Klammer nicht vergessen!)
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

