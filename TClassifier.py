import sys
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics
from time import strftime, localtime, time
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.model_selection import KFold
from scipy.stats import sem


"""Build a twitter harassment detector model

   This code uses script obtained from scikit-learn tutorial, specifically exercise 02 of 
   the tutorial.  Tutorial url: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
        Author: Olivier Grisel <olivier.grisel@ensta.org>
        License: Simplified BSD        
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Sep 21, 2017 at 09:46:01'
__email__ = 'pvargas@cs.odu.edu'


def classifier(harassment_data_folder):
    """
    :param harassment_data_folder: folder where dataset classification sub-folders reside
    :return: void
    """

    print('\nLoading harassment dataset files....')
    dataset = load_files(harassment_data_folder, shuffle=False)

    """
    # test with 20_newsgroup
    categories = ['alt.atheism', 'soc.religion.christian',
                  'comp.graphics', 'sci.med']
    dataset = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
    """

    print("n_samples: %d" % len(dataset.data))

    # split the dataset in training and test set to obtain metrics classification:
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.1, random_state=None)

    # create k-fold cross validation
    cv = KFold(10, shuffle=True, random_state=None)

    # build a vectorizer / classifier pipeline that filters out tokens that are too rare or too frequent
    pipeline = Pipeline([
        ('vect', TfidfVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(loss='hinge', penalty='l2',
                              alpha=1e-5, random_state=42,
                              max_iter=5, tol=None)),
    ])

    # make cross-fold validation using training data
    scores = cross_val_score(pipeline, docs_train, y_train, cv=cv)
    print('\nScores,', scores)

    pipeline.fit(docs_train, y_train)

    """
    build a grid search to find out whether unigrams or bigrams are more useful.
    Fit the pipeline on the training set using grid search for the parameters
    """

    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2)],
    }
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
    grid_search.fit(dataset.data, dataset.target)


    """
    print the mean and std for each candidate along with the parameter
    settings for all the candidates explored by grid search.

    n_candidates = len(grid_search.cv_results_['params'])

    for i in range(n_candidates):
        print(i, 'params - %s; mean - %0.2f; std - %0.2f'
                 % (grid_search.cv_results_['params'][i],
                    grid_search.cv_results_['mean_test_score'][i],
                    grid_search.cv_results_['std_test_score'][i]))

    new_doc = [
        "@handle1 your cat is so pretty. Can I pass by your home an pet it?",
        "@Lesdoggg I take the worst pics ever!! Thank God Beyoncé is just fucking beautiful!! Thanks for pic Queen B!! I was so nervous!!",
        "Replying to @Boobafett69 @Lesdoggg Tough woman! I bet the Trumpster wouldn't dis her. She would make him wet his diaper. Beautiful"
    ]

    """
    new_doc = []
    no_doc = 50
    for folder in os.listdir(path):
        print(folder)
        print(os.listdir(path + folder))
        for tweet_file in os.listdir(path + folder)[:no_doc]:
            tweet_fhs = open(path + folder + '/' + tweet_file, "r", encoding='iso-8859-1')
            new_doc.append(tweet_fhs.read())
            tweet_fhs.close()

    predictions = cross_val_predict(pipeline, docs_test, y_test, cv=cv)

    print("Mean score: {0:.3f} (+/-{1:.3f})".format(np.mean(scores), sem(scores)))
    accuracy = metrics.r2_score(y_test, predictions)
    print("accuracy ---> ", accuracy)

    # predict the outcome on the testing set and store it in a variable named y_predicted
    y_predicted = pipeline.predict(new_doc)

    print()
    print('Prediction index ===> ', y_predicted)
    print()

    counter = 0
    for doc, category in zip(new_doc, y_predicted):
        counter += 1
        print('<%d> %r => %s' % (counter, doc, dataset.target_names[category]))

    # predict the outcome on the testing set and store it in a variable named y_predicted
    y_predicted = pipeline.predict(docs_test)

    # Print the classification report
    print(metrics.classification_report(y_test, y_predicted,
                                        target_names=dataset.target_names))

    #import matplotlib.pyplot as plt
    #plt.matshow(cm)
    #plt.show()

    return


if __name__ == '__main__':
    """
    :param path: folder where dataset classification sub-folders reside

    testing argument:
    /home/hamar/scikit_learn_data/scikit-learn-master/doc/tutorial/text_analytics/data/movie_reviews/txt_sentoken/
        
    """

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # checks if path was passed as an argument
    if len(sys.argv) != 2:
        print('Usage: python3 TClassifier.py <corpus_folder>')
        sys.exit(-1)

    path = sys.argv[1]

    if not os.path.isdir(path):
        print('\nPath provided <<%s>> MUST be a folder.' % path)
        print('Usage: python3 TClassifier.py <corpus_folder>')
        sys.exit(-1)

    classifier(path)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
