conv_data <- read.csv("deletions.csv")

conv_matrix <- data.matrix(conv_data[17:91])
final_value <- as.data.frame(t(conv_matrix))
colnames(final_value) <- conv_data$Handle

liberal <- c("blue")
conservative <- c("red")
neutral <- c("black")
unknown <- c("magenta")

get_color <- as.data.frame(t(data.frame(liberal, conservative, 
                                        neutral, unknown)))
colnames(get_color) <- "Color"

element <- 0
for (k in names(final_value)){
  conv_vector <- final_value[[k]]

  element <- element + 1
  counter <- 0    # Number of Conversations for a particular handle
  
  for (i in conv_vector) {  
    counter <- counter + 1
      if (is.na(i)) 
        break
    }

  sort(conv_vector, decreasing = TRUE)

  vtu <- k
  
  for (extractName in conv_data$Name[element]){
    fullname <- extractName
    break
  }
  
  for (extractStance in conv_data$Stance[element]){
    stance <- extractStance
    break
  }
  
  element_std <- conv_data$std[element]
  
  for (extractSex in conv_data$Sex[element]){
    sex <- extractSex
    break
  }
  
  
  if (tolower(sex) == 'female')
    pitch_symbol <- 1
  else
    pitch_symbol <- 3

  for (extractColor in get_color$Color[stance]){
    symbol_color <- extractColor
    break
  }
  
  followers = format(conv_data$Followers[element], big.mark=",", scientific=FALSE)
  
  g_title <- paste("Deleted Accounts in ", fullname, "Conversations\n",
                   "Sex=", sex, " Stance=", stance, 
                   " STD=", element_std, "\n",
                   "Response per Tweet=", conv_data$Ave.Response[element],
                   " Followers=", followers)
  plot(sort(conv_vector, decreasing = TRUE), col=symbol_color,
       pch=pitch_symbol,
       xlab="Conversation", ylab = "Deleted Accounts", main = g_title)
}

