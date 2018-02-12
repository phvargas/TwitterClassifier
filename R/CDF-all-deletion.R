susdata <- read.csv("/home/pvargas/TwitterHarassment/TwitterClassifier/data/account_suspended_deleted.csv")

library("ggplot2")

df <- data.frame(harasers = cumsum(sort(susdata$susp.closed)), sex=susdata$sex)
p5 <- ggplot(df, aes(df$harasers)) + stat_ecdf(geom='line') +
  scale_x_continuous(name='Number of Suspended/Deleted Accounts') +
  scale_y_continuous(name='Percentage') +
  ggtitle("CDF for Deleted/Suspended Account in Observed Conversations") +
  theme(plot.title = element_text(hjust = 0.5))
p5 

reduce_df <- subset(susdata, sex=='female')
p4 <- ggplot(reduce_df, aes(cumsum(sort(reduce_df$susp.closed)))) + stat_ecdf(geom='line', color='orange') +
  scale_x_continuous(name='Number of Suspended/Deleted Accounts') +
  scale_y_continuous(name='Percentage') +
  ggtitle("CDF for Deleted/Suspended Accounts in Observed Female Conversations") +
  theme(plot.title = element_text(hjust = 0.5))
p4 

reduce_df <- subset(susdata, sex=='male')
p3 <- ggplot(reduce_df, aes(cumsum(sort(reduce_df$susp.closed)))) + stat_ecdf(geom='line', color='blue') +
  scale_x_continuous(name='Number of Suspended/Deleted Accounts') +
  scale_y_continuous(name='Percentage') +
  ggtitle("CDF for Deleted/Suspended Accounts in Observed Male Conversations") +
  theme(plot.title = element_text(hjust = 0.5))
p3 

reduce_df <- subset(susdata, stance=='conservative')
p2 <- ggplot(reduce_df, aes(cumsum(sort(reduce_df$susp.closed)))) + stat_ecdf(geom='line', color='red') +
  scale_x_continuous(name='Number of Suspended/Deleted Accounts') +
  scale_y_continuous(name='Percentage') +
  ggtitle("CDF for Deleted/Suspended Accounts in Observed Conservative Conversations") +
  theme(plot.title = element_text(hjust = 0.5))
p2

reduce_df <- subset(susdata, stance=='liberal')
p1 <- ggplot(reduce_df, aes(cumsum(sort(reduce_df$susp.closed)))) + stat_ecdf(geom='line', color='blue') +
  scale_x_continuous(name='Number of Suspended/Deleted Accounts') +
  scale_y_continuous(name='Percentage') +
  ggtitle("CDF for Deleted/Suspended Accounts in Observed Liberal Conversations") +
  theme(plot.title = element_text(hjust = 0.5))
p1
