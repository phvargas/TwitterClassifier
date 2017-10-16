import sys
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import load_files
from time import strftime, localtime, time


"""
   Script finds records with close similarity in a corups    
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Sun,  Oct 15, 2017 at 11:56:16'
__email__ = 'pvargas@cs.odu.edu'


def duplicates(harassment_data_folder):
    """
    :param harassment_data_folder: folder where dataset classification sub-folders reside
    :return: void
    """
    encoding = 'utf-8'
    fh = open('SimilarDocs.data', 'w')

    print('\nLoading harassment dataset files....')
    dataset = load_files(harassment_data_folder, shuffle=False)

    print('Vectorizing dataset....')
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(dataset.data)

    print('Creating TFIDF matrix....')
    mtx = (tfidf * tfidf.T).A

    # find matrix size
    row = mtx.shape[0]
    col = mtx.shape[1]

    # tweet filename has the format tweet00099.txt, doc_idx is a set to contain numerical section of repeated tweets
    doc_idx = set()
    similar_docs = []
    counter = 0
    mix_counter = 0
    for x in range(0, row):
        for y in range(x, col):
            idx = re.search('(\d+).txt', dataset.filenames[y]).group(1)
            if y == x and idx not in doc_idx:
                if len(similar_docs) > 1:
                    counter += 1

                    print()
                    fh.write('\n')
                    clf = ''
                    class_is_same = True
                    for doc in similar_docs:
                        if 'no_harassment' in doc:
                            if clf and clf != 'no_harassment':
                                class_is_same = False
                            clf = 'no_harassment'
                        elif clf and clf != 'harassment':
                            class_is_same = False
                            clf = 'harassment'
                        else:
                            clf = 'harassment'

                        print(doc)
                        fh.write('{0}\n'.format(doc))

                    if not class_is_same:
                        print('Mix classification')
                        fh.write('{0}\n'.format('Mix classification'))
                        mix_counter += 1

                doc_idx.add(idx)
                similar_docs = ['<{0}>  {1}  {2}:'.format(idx,
                                                          dataset.target_names[dataset.target[y]],
                                                          dataset.data[y].decode(encoding))]

            elif mtx[x][y] >= 0.90 and idx not in doc_idx:
                doc_idx.add(idx)
                similar_docs.append('<{0}>  {1}  {2}:'.format(idx,
                                                              dataset.target_names[dataset.target[y]],
                                                              dataset.data[y].decode(encoding)))
    print()
    print()
    fh.write('\n\n')

    print('Number of mix classification cluster: ', mix_counter)
    fh.write('Number of mix classification cluster: {0}\n'.format(mix_counter))

    print('Total number of clusters:', counter)
    fh.write('Total number of clusters:: {0}\n'.format(counter))

    fh.close()

    return


if __name__ == '__main__':
    """
    :param path: folder where dataset classification sub-folders reside
       
    """

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # checks if path was passed as an argument
    if len(sys.argv) != 2:
        print('Usage: python3 CheckDuplicate.py <corpus_folder>')
        sys.exit(-1)

    path = sys.argv[1]

    if not os.path.isdir(path):
        print('\nPath provided <<%s>> MUST be a folder.' % path)
        print('Usage: python3 CheckDuplicate.py <corpus_folder>')
        sys.exit(-1)

    duplicates(path)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
