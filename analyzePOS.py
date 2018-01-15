from textblob import TextBlob
import sys
import os
from sklearn.datasets import load_files
from sklearn.feature_extraction import text

if len(sys.argv) < 2:
    print('Usage: python3 analyzePOS.py <corpus_folder>')
    sys.exit(-1)

folder = sys.argv[1]
if not os.path.isdir(folder):
    print('Corpus path MUST be a directory')
    print('Usage: python3 analyzePOS.py <corpus_folder>')
    sys.exit(-1)

corpus = folder.split("/")[-1]
if not corpus:
    corpus = folder.split("/")[-2]

print('Loading corpus %s' % corpus)
dataset = load_files(folder, shuffle=False)

print('Removing stopwords....')
stop_words = text.ENGLISH_STOP_WORDS.union(['https', 'http'])


print('Transforming documents to TFIDF representation ...')

counter = 0
for document, cat in zip(dataset.data, dataset.target):
    if cat == 0:
        counter += 1
        print(document.decode('utf-8'))

print(counter)
