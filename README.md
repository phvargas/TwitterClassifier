# Twitter Classifier

Module applies supervised machine learning method to predict the classification of a body of text.


## TClassifier

TClassifier takes as parameter the path where the working corpus resides, in order to train and validate its documents.
The script creates a persistent model saved on a pickle file named after the corpus' name and the algorithm utilized to train
the model. For example, if a path where the corpus resides is /data/typeOfThing and SVM is the selected SVM algorithm,
the persistent model will be saved as models/typeOfThings_svm.pkl

### List of algorithm parameters
parameter    description
-----------------------------------------
svc          LinearSVC
mnb          MultinomialNB
ncentroid    Nearest Centroid
ridge        Ridge
knn          KNeighbors
pac          Passive Aggressive
rndforrest   Random Forrest
perceptron   Perceptron
bernoulli    BernoulliNB
sgd          Stochastic Gradient Descent
