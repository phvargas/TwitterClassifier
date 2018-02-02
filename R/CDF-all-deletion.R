susdata <- read.csv("/home/hamar/data/odu/TwitterClassifier/data/account_suspended_deleted.csv")
df <- data.frame(harasers = cumsum(sort(susdata$susp.closed)))
p5 <- ggplot(df, aes(df$harasers)) + stat_ecdf(geom='line') +
  scale_x_continuous(name='Number of Suspended/Deleted Accounts') +
  scale_y_continuous(name='Percentage') +
  ggtitle("CDF for Deleted/Suspended Account in Observed Conversations") +
  theme(plot.title = element_text(hjust = 0.5))
p5 
