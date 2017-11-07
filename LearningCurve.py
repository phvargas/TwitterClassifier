import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction import text
from sklearn import svm
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit, KFold
from time import strftime, localtime, time


def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")

    print('Getting training score values ....')
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

# record running time
start = time()
print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

folder_model = 'data/dataset/no_ambiguous/'
dataset = load_files(folder_model, shuffle=False)

stop_words = text.ENGLISH_STOP_WORDS.union(['https', 'http'])
count_vect = CountVectorizer(analyzer='word', strip_accents='unicode', stop_words='english')
tfidf_transformer = TfidfTransformer()

X = count_vect.fit_transform(dataset.data)
y = dataset.target


#title = "Learning Curves (SGD algorithm / crawl_tweets_26_74 dataset)"
title = "Learning Curves (SVM algorithm / no_ambiguous dataset)\nkernel=linear"
# Cross validation with 100 iterations to get smoother mean test and train
# score curves, each time with 20% data randomly selected as a validation set.
n_splits = 100
cv = ShuffleSplit(n_splits=n_splits, test_size=0.1, random_state=None)
#cv = KFold(n_splits, shuffle=True, random_state=None)
"""
estimator = SGDClassifier(loss='modified_huber', penalty='l2',
                          alpha=1e-5, random_state=42,
                          max_iter=5, tol=None)
"""
estimator = svm.SVC(C=1.0, cache_size=8000, class_weight=None, coef0=0.0, degree=3,
                    gamma='auto', kernel='linear', max_iter=-1, probability=True, random_state=None,
                    shrinking=True, tol=0.001, verbose=False)

plot_learning_curve(estimator, title, X, y, ylim=(0.7, 1.01), cv=cv, n_jobs=4)

print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
exec_time = time() - start
print('Execution Time: %.2f seconds or %2.f minutes' % (exec_time, exec_time / 60))

plt.show()
