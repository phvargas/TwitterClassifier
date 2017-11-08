import sys
import os
import re
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import Utilities.ConvertDataType as conv
import algorithms.TextClassifiers as alg
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics, linear_model
from time import strftime, localtime, time
from sklearn.model_selection import cross_val_score, cross_val_predict, cross_validate, KFold
from scipy.stats import sem
from matplotlib import pyplot as plt
from sklearn.externals import joblib


"""Build a twitter harassment classification model

TClassifier takes as parameter the path where the working corpus resides, in order to train and validate its documents.
The script creates a persistent model saved on a pickle file named after the corpus' name and the algorithm utilized to train
the model. For example, if a path where the corpus resides is /data/typeOfThing and SVM is the selected SVM algorithm,
the persistent model will be saved as models/typeOfThings_svm.pkl

## List of algorithm parameters
parameter    description
========================
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
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Sep 21, 2017 at 09:46:01'
__email__ = 'pvargas@cs.odu.edu'


def classifier(harassment_data_folder, clf_alg):
    """
    :param harassment_data_folder: folder where dataset classification sub-folders reside
    :return: void
    """
    encoding = 'utf-8'
    # get title from folder dataset name
    title = harassment_data_folder.split('/')
    if title[-1] == '':
        title.pop()

    title = title[-1]

    # Create linear regression object
    regr = linear_model.LinearRegression()

    print('\nLoading harassment dataset files....')
    dataset = load_files(harassment_data_folder, shuffle=False)

    print("n_samples: %d" % len(dataset.data))

    # split the dataset in training and test set to obtain metrics classification:
    docs_train, docs_test, y_train, y_test, train_filenames, test_filenames = train_test_split(
        dataset.data, dataset.target, dataset.filenames, test_size=0.1, random_state=None)

    # create k-fold cross validation
    k_fold = 10
    cv = KFold(k_fold, shuffle=True, random_state=None)

    # build a vectorizer / classifier pipeline that filters out tokens that are too rare or too frequent
    """
    :parameter for SGDClassifier(loss='modified_huber', penalty='l2',
                                 alpha=1e-5, random_state=42,
                                 max_iter=5, tol=None))

    :parameter default for svm.SVC(C=1.0, cache_size=7000, class_weight=None, coef0=0.0, degree=3,
                                   gamma='auto', kernel='rbf', max_iter=-1, probability=True, random_state=None,
                                   shrinking=True, tol=0.001, verbose=False))
    """

    clf = Pipeline([
        ('vect', TfidfVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', clf_alg),
    ])

    # make cross-fold validation using training data
    print('Obtaining %d-fold validation scores' % k_fold)
    scores = cross_val_score(clf, docs_train, y_train, cv=cv)
    print('\nScores,', scores)

    # predictions = cross_val_predict(pipeline, docs_test, y_test, cv=cv)
    print('Obtaining cross validation predictions to test set ....')
    predictions = cross_val_predict(clf, docs_test, y_test, cv=cv)

    """
    y = dataset.target
    trace1 = go.Scatter(x=y, y=predictions, mode='markers',
                        marker=dict(size=8,
                                    color='rgb(0, 0, 255)',
                                    line=dict(
                                        width=2,
                                        color='rgb(0, 0, 0)'))
                        )

    trace2 = go.Scatter(x=[y.min(), y.max()], y=[y.min(), y.max()],
                        line=dict(color='rgb(0, 0, 0)',
                                  width=5, dash='dash')
                        )

    layout = go.Layout(showlegend=False,
                       yaxis=dict(
                           range=[0, 2],
                           zeroline=False,
                           title='Predicted'),
                       xaxis=dict(
                           title='Measured', )
                       )
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    py.plot(fig, filename="c-v-predict")
    """
    print('predictions: ', predictions, 'size:', len(predictions))

    # write no_harassment false positive and false negative into a file
    fhs = open('remove_documents.dat', mode='w')

    red_dots = []
    red_prob = []
    blue_dots = []
    blue_prob = []

    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    X_train_counts = count_vect.fit_transform(docs_test)

    print('X_train_Counts length', X_train_counts.shape)
    print('Number of documents:', len(docs_test))

    X_data = tfidf_transformer.fit_transform(X_train_counts)
    print('X_data type:', type(X_data))

    counter = 0
    bin = {'0-2': 0, '2-3': 0, '3-3.5': 0, '3.5-': 0}

    for x in range(len(predictions)):
        if predictions[x] != y_test[x]:
            red_dots.append(x)
            counter += 1
            """
            print('<{0}> {1} => {2} file ==> {3}'.format(counter, docs_test[x].decode(encoding),
                                                         dataset.target_names[y_predicted[x]],
                                                         get_filename_sequence(test_filenames[x])))                                                         
            """
            tfidf_sum = sum(X_data[counter].toarray()[0])

            if tfidf_sum <= 2:
                bin['0-2'] += 1
            elif tfidf_sum <= 3:
                bin['2-3'] += 1
            elif tfidf_sum <= 3.5:
                bin['3-3.5'] += 1
            else:
                bin['3.5-'] += 1
        else:
            blue_dots.append(x)
    print(bin)
    for key in bin:
        print('%s,%d' % (key, bin[key]))

    fhs.close()

    # Print the classification report
    print()
    print(metrics.classification_report(y_test, predictions,
                                        target_names=dataset.target_names))

    print()

    print("  {0}-fold cross validation mean score: {1:.3f} (+/-{2:.3f})".format(k_fold, np.mean(scores), sem(scores)))
    rsqr_score = metrics.r2_score(y_test, predictions)
    print("  R^2 score ---> ", rsqr_score)
    print('  accuracy', metrics.accuracy_score(y_test, predictions))

    print()
    print("  {0} dataset size: {1}".format(title, len(dataset.data)))
    print("  test sample size: {0}".format(len(docs_test)))
    print("  number of false positive + false negative: {0}  --->  {1:.0f}%".format(len(red_dots), len(red_dots)/len(docs_test) * 100))

    print()
    print('Writing persistence model...')
    filename = 'models/' + title + '.pkl'
    joblib.dump(clf, filename)

    # preserve categories
    filename = 'models/' + title + '_category.pkl'
    #joblib.dump(dataset.target_names, filename)

    # Print and plot the confusion matrix
    cm = metrics.confusion_matrix(y_test, predictions)

    print(cm)
    print()

    display_conf_table(cm, dataset.target_names)

    # plot scatter plot
    #plt.scatter(blue_dots, blue_prob, label='true positive + true negative')
    #plt.scatter(red_dots, red_prob, color='red', label='false positive + false negative')
    #plt.title(title + " Predicted Category Probability")
    #plt.xlabel("Tweet_index")
    #plt.ylabel("Pr(category | tweet) * tweet_index")
    #plt.legend()

    #import matplotlib.pyplot as plt
    #plt.matshow(cm)
    #plt.show()

    print('Test doc size:', len(docs_test))
    print(docs_test[0])

    return


def display_conf_table(arr, categories):
    row = arr.shape[0]
    col = arr.shape[1]
    print("Actual Class".rjust(56))

    print(' ' * 35, end='')
    for x in range(0, row):
        print("  %s" % categories[x], end="")
    print()

    for x in range(0, row):
        for y in range(0, col):
            if y == 0:
                predict_text = 'Predicted Cls ' + categories[x]
                print(' {0:>30} => '.format(predict_text), end='')

            print('{0:12d}   '.format(arr[x, y]), end='')
        print()

    return


def get_filename_sequence(file_path):
    try:
        regex = re.search("(\d+)", file_path.split('/')[-1]).group(1)

    except AttributeError:
        regex = None

    return regex


if __name__ == '__main__':
    """
    :param path: folder where dataset classification sub-folders reside       
    """

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # checks if path was passed as an argument
    if len(sys.argv) < 3:
        print('\nNot enough arguments..')
        print('Usage: python3 TClassifier.py <corpus_folder> <algorithm="algorithm"> params:')
        sys.exit(-1)

    path = sys.argv[1]

    if not os.path.isdir(path):
        print('\nPath provided <<%s>> MUST be a folder.' % path)
        print('Usage: python3 TClassifier.py <corpus_folder> <algorithm="algorithm"> params:')
        sys.exit(-1)

    params = sys.argv[2].split('=')
    if params[0] != 'algorithm':
        print('\nSecond parameter %s needs to be of the form algorithm=algorithm_type' % sys.argv[2])
        print('Usage: python3 TClassifier.py <corpus_folder> <algorithm=algorithm_type> params:')
        print('Example: python3 TClassifier.py /data/my_corpus algorithm=sdg')
        sys.exit(-1)

    params = conv.list2kwarg(sys.argv[2:])

    """
    SGDClassifier params example:
    algorithm=sgd loss=modified_huber penalty=l2 alpha=1e-5 random_state=42 max_iter=5 tol=None
    
    
    """
    algorithm = alg.get_algorithm(**params)
    if params:
        if algorithm:
            classifier(path, algorithm)
    else:
        print('\nError: parameters provided  NOT valid {0}'.format(sys.argv[2:]))
        print('Usage: python3 TClassifier.py <corpus_folder> <algorithm=algorithm_type> params:')
        print('Example: python3 TClassifier.py /data/my_corpus algorithm=sdg')

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    exec_time = time()-start
    print('Execution Time: %.2f seconds or %2.f minutes' % (exec_time, exec_time / 60))
sys.exit(0)
