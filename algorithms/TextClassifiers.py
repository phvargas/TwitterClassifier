from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier


def get_algorithm(**kwargs):
    algorithm_list = {
        'sgd': 'Stochastic Gradient Descent',
        'ridge': 'Ridge',
        'perceptron': 'Perceptron',
        'pac': 'Passive Aggressive',
        'knn': 'KNeighbors',
        'rndforrest': 'Random Forrest',
        'ncentroid': 'Nearest Centroid',
        'mnb': 'MultinomialNB',
        'bernoulli': 'BernoulliNB',
        'svc': 'LinearSVC'
    }

    clf = 0
    if 'algorithm' not in kwargs:
        return clf

    algorithm = kwargs['algorithm']
    kwargs.pop('algorithm', None)

    for key in kwargs:
        try:
            kwargs[key] = eval(kwargs[key])
        except NameError:
            pass

    if algorithm == 'sgd':
        clf = SGDClassifier(**kwargs)
    elif algorithm == 'ridge':
        clf = RidgeClassifier(**kwargs)
    elif algorithm == 'perceptron':
        clf = Perceptron(**kwargs)
    elif algorithm == 'pac':
        clf = PassiveAggressiveClassifier(**kwargs)
    elif algorithm == 'knn':
        clf = KNeighborsClassifier(**kwargs)
    elif algorithm == 'rndforrest':
        clf = RandomForestClassifier(**kwargs)
    elif algorithm == 'ncentroid':
        clf = NearestCentroid(**kwargs)
    elif algorithm == 'mnb':
        clf = MultinomialNB(**kwargs)
    elif algorithm == 'bernoulli':
        clf = BernoulliNB(**kwargs)
    elif algorithm == 'svc':
        clf = LinearSVC(**kwargs)
    else:
        print('Error: algorithm specified not included in the list. Use any parameter shown below:')
        print()
        print('parameter    description')
        print('=' * len('parameter    description'))

        for key in algorithm_list:
            print('{0:<13}{1}'.format(key, algorithm_list[key]))

    return clf
