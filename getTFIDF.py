import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

print('Loading dataset ....')
folder = 'data/dataset/no_ambiguous/'
dataset = load_files(folder, shuffle=False)

print(dataset.data)

stop_words = text.ENGLISH_STOP_WORDS.union(['https', 'http'])

count_vect = CountVectorizer(analyzer='word', strip_accents='unicode', stop_words=stop_words)
tfidf_transformer = TfidfTransformer()
X_counts = count_vect.fit_transform(dataset.data)

print('X_Counts length', X_counts.shape)
print('Number of documents:', len(dataset.data))

X = tfidf_transformer.fit_transform(X_counts)
print('X_data type:', type(X))

bin = {'0-2': 0, '2-3': 0, '3-3.5': 0, '3.5-': 0}

for feature in X:
    tfidf_sum = sum(feature.toarray()[0])
    if tfidf_sum <= 2:
        bin['0-2'] += 1
    elif tfidf_sum <= 3:
        bin['2-3'] += 1
    elif tfidf_sum <= 3.5:
        bin['3-3.5'] += 1
    else:
        bin['3.5-'] += 1

print(bin)
for key in bin:
    print('%s,%d' % (key, bin[key]))
