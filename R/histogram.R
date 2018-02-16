freq_data <- read.csv("SeanHannity-freq-count.csv")

fullname <- "Sean Hannity"
g_title <- paste("Histogram of Repeated Accounts\n", "in ", fullname, " Conversations")
barplot(freq_data$Freq, names.arg=freq_data$Account_Appearance, log="y", ylim=c(1, 5000), col="red",
        ylab = "Frequency of Repetition", xlab="Number of Repeated Accounts", main = g_title)

freq_data <- read.csv("HillaryClinton-freq-count.csv")

fullname <- "Hillary Clinton"
g_title <- paste("Histogram of Repeated Accounts\n", "in ", fullname, " Conversations")
barplot(freq_data$Freq, names.arg=freq_data$Account_Appearance, log="y", ylim=c(1, 5000), col="blue",
        ylab = "Frequency of Repetition", xlab="Number of Repeated Accounts", main = g_title)


freq_data <- read.csv("BillKeller-freq-count.csv")

fullname <- "Bill Keller"
g_title <- paste("Histogram of Repeated Accounts\n", "in ", fullname, 
                 " Conversations\n Unknown Political Stance")
barplot(freq_data$Freq, names.arg=freq_data$Account_Appearance, ylim=c(0, 50), col="green",
        ylab = "Frequency of Repetition", xlab="Number of Repeated Accounts", main = g_title)



freq_data <- read.csv("all-freq-count.csv")
fullname <- "All"
g_title <- paste("Histogram of Repeated Accounts\n", "in ", fullname, " Conversations")

barplot(freq_data$Freq, names.arg=freq_data$Account_Appearance, log="y", ylim=c(1, 1000000), col="gray",
     ylab = "Frequency of Repetition", xlab="Number of Repeated Accounts", main = g_title)

