import sys
import os
import re
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
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
    clf = Pipeline([
        ('vect', TfidfVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(loss='modified_huber', penalty='l2',
                              alpha=1e-5, random_state=42,
                              max_iter=5, tol=None)),
    ])

    # make cross-fold validation using training data
    scores = cross_val_score(clf, dataset.data, dataset.target, cv=cv)
    print('\nScores,', scores)

    # predictions = cross_val_predict(pipeline, docs_test, y_test, cv=cv)
    predictions = cross_val_predict(clf, dataset.data, dataset.target, cv=cv)

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

    print('predictions: ', predictions, 'size:', len(predictions))

    # predict the outcome on the testing set and store it in a variable named y_predicted
    clf.fit(docs_train, y_train)
    y_predicted = clf.predict(docs_test)
    y_prob = clf.predict_proba(docs_test)

    # write no_harassment false positive and false negative into a file
    fhs = open('remove_documents.dat', mode='w')

    red_dots = []
    red_prob = []
    blue_dots = []
    blue_prob = []
    counter = 0
    for x in range(len(y_predicted)):
        if y_predicted[x] != y_test[x]:
            red_dots.append(x)
            red_prob.append(y_prob[x][y_predicted[x]] * x)
            counter += 1
            """
            print('<{0}> {1} => {2} file ==> {3}'.format(counter, docs_test[x].decode(encoding),
                                                         dataset.target_names[y_predicted[x]],
                                                         get_filename_sequence(test_filenames[x])))                                                         
            """
            if dataset.target_names[y_predicted[x]] == 'harassment':
                #print(test_filenames[x])
                fhs.write('%s\n' % test_filenames[x])
        else:
            blue_dots.append(x)
            blue_prob.append(y_prob[x][y_predicted[x]] * x)
    fhs.close()

    # Print the classification report
    print()
    print(metrics.classification_report(y_test, y_predicted,
                                        target_names=dataset.target_names))

    print()

    print("  {0}-fold cross validation mean score: {1:.3f} (+/-{2:.3f})".format(k_fold, np.mean(scores), sem(scores)))
    rsqr_score = metrics.r2_score(dataset.target, predictions)
    print("  R^2 score ---> ", rsqr_score)
    print('  accuracy', metrics.accuracy_score(dataset.target, predictions))

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
    joblib.dump(dataset.target_names, filename)

    # Print and plot the confusion matrix
    cm = metrics.confusion_matrix(y_test, y_predicted)

    print(cm)
    print()

    display_conf_table(cm, dataset.target_names)

    # plot scatter plot
    plt.scatter(blue_dots, blue_prob, label='true positive + true negative')
    plt.scatter(red_dots, red_prob, color='red', label='false positive + false negative')
    plt.title(title + " Predicted Category Probability")
    plt.xlabel("Tweet_index")
    plt.ylabel("Pr(category | tweet) * tweet_index")
    plt.legend()

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
