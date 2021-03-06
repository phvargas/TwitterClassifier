import numpy as np
import sys
import os
from sklearn.datasets import load_files
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer

if len(sys.argv) < 2:
    print('Usage: python3 getTerms.py <corpus_folder>')
    sys.exit(-1)

folder = sys.argv[1]
if not os.path.isdir(folder):
    print('Corpus path MUST be a directory')
    print('Usage: python3 getTerms.py <corpus_folder>')
    sys.exit(-1)

corpus = folder.split("/")[-1]
if not corpus:
    corpus = folder.split("/")[-2]

print('Loading corpus %s' % corpus)
dataset = load_files(folder, shuffle=False)

print('Removing stopwords....')
stop_words = text.ENGLISH_STOP_WORDS.union(['https', 'http'])

token_pattern = '(?u)\\b\\w\\w+\\b|@|#[\w\d_]*'
count_vect = CountVectorizer(strip_accents='unicode', stop_words=stop_words, token_pattern=token_pattern)

print('Transforming documents to TFIDF representation ...')
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
    print('%s,%d,combined' % (key, term_freq[key]))

fhs = open('/home/hamar/data/odu/golbeck/tweets/zipt-data.dat', mode='w')
fhs.write('word\tvalue\n')

for key in sorted(term_freq, key=term_freq.get, reverse=True):
    print('%s,%d,combined' % (key, term_freq[key]))
    fhs.write('{}\t{}\n'.format(key, term_freq[key]))


fhs.close()
