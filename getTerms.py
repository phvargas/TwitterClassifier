import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

folder = 'data/dataset/no_ambiguous/no_harassment/'
dataset = load_files(folder, shuffle=False)

print(dataset.data)

stop_words = text.ENGLISH_STOP_WORDS.union(['https', 'http'])

count_vect = CountVectorizer(analyzer='word', strip_accents='unicode', stop_words=stop_words)
tfidf_transformer = TfidfTransformer()
X = count_vect.fit_transform(dataset.data)

corpus_terms = list(zip(count_vect.get_feature_names(), np.asarray(X.sum(axis=0)).ravel()))

term_freq = {}
counter = 0
for term, freq in corpus_terms:
    counter += 1
    print(term, freq, counter)
    term_freq[term] = freq

print()
print('term,freq,category')
for key in sorted(term_freq, key=term_freq.get, reverse=True)[:50]:
    print('%s,%d,no_harassment' % (key, term_freq[key]))
