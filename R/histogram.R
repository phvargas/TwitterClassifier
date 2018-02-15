freq_data <- read.csv("data/SeanHannity-freq-count.csv")

fullname <- "Sean Hannity"

g_title <- paste("Histogram of ", fullname, "\nAccounts Reappearance in Conversation")

#hist(x = freq_data$Account_Appearance, ylim = freq_data$Freq,
#     xlab="Account Repetition", ylab = "Frequency", main = g_title)

barplot(freq_data$Freq, names.arg=freq_data$Account_Appearance, log="y", ylim=c(1, 5000), col="red",
     ylab = "Frequency of Reappearance", xlab="Number of Accounts Reaperance", main = g_title)
