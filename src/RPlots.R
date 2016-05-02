library('plotrix')
library('ggplot2')
mydata <- read.csv(file = "processedData.csv",header = TRUE, sep = ',')

#qplot(data = mydata, search_term, age)
#qplot(data = mydata, location,age,color=search_term)

#graph3
qplot(data = mydata, search_term, facets = .~location, fill=search_term)
ggsave (filename = "Twitter_Location_Based.png")

#qplot(data = mydata, location,age, color=score,geom = c("point","smooth"))

# histogram showing age of tweeters for candidates
#qplot(data = mydata, age, fill=search_term, binwidth=20)

#graph1
qplot(data = mydata, age, fill=search_term, binwidth=5)
ggsave (filename = "Twitter_Age_Based.png")

#qplot(data = mydata, log(age), fill=search_term, binwidth=20)
#qplot(data = mydata, age, location, facets = .~search_term , fill=search_term)
#qplot(data = mydata, age, location, facets = .~search_term , color=search_term)

#graph2
qplot(data = mydata, score, geom='density', facets = .~search_term, fill=search_term)
ggsave (filename = "Twitter_SentimentScore_Based.png")

#qplot(data = mydata, location, geom='density',facets = .~search_term, color=search_term)
#qplot(data = mydata, score ,facets = .~search_term,bins=30) + geom_bar()


par(mfrow=c(1,1))
slices <- c(nrow(subset(subset(mydata,search_term=="hillary"),score>0)),nrow(subset(subset(mydata,search_term=="hillary"),score<0)),nrow(subset(subset(mydata,search_term=="hillary"),score==0)) )
lbls   <- c("Yes","No","Neutral")
pct <- round(slices/sum(slices)*100)
lbls2 <- paste(lbls, " ", pct, "%", sep="")
pie(slices, labels=lbls2, col=rainbow(length(lbls2)),main="Sentiment Analysis for Hillary")
jpeg(file = "HIllary_chart.jpg")


par(mfrow=c(1,1))
slices <- c(nrow(subset(subset(mydata,search_term=="trump"),score>0)),nrow(subset(subset(mydata,search_term=="trump"),score<0)),nrow(subset(subset(mydata,search_term=="trump"),score==0)) )
lbls   <- c("Yes","No","Neutral")
pct <- round(slices/sum(slices)*100)
lbls2 <- paste(lbls, " ", pct, "%", sep="")
pie(slices, labels=lbls2, col=rainbow(length(lbls2)),main="Sentiment Analysis for Trump")
png(file = "trump_chart.jpg")

par(mfrow=c(1,1))
slices <- c(nrow(subset(subset(mydata,search_term=="bernie"),score>0)),nrow(subset(subset(mydata,search_term=="bernie"),score<0)),nrow(subset(subset(mydata,search_term=="bernie"),score==0)) )
lbls   <- c("Yes","No","Neutral")
pct <- round(slices/sum(slices)*100)
lbls2 <- paste(lbls, " ", pct, "%", sep="")
pie(slices, labels=lbls2, col=rainbow(length(lbls2)),main="Sentiment Analysis for Bernie Sanders")
png(file = "bernie_chart.png")





