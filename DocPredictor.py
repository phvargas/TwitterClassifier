import sys
import os
import re
from time import strftime, localtime, time
from sklearn.externals import joblib


"""
    Given a set of documents contained in a file classified the documents based on a provided persistent model.     
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  Oct 16, 2017 at 13:44:27'
__email__ = 'pvargas@cs.odu.edu'


def predict(model, category_path, doc):
    """
    :param model: folder where dataset classification sub-folders reside
    :param category_path: path where category model resides
    :param doc: path of document to be compared
    :return: void
    """
    remove_tco = re.compile('https?:\\?\s?/\\?\s?/t.co\\?\s?/\S+')
    remove_hdl = re.compile('@\S+')

    # load model into pipeline object
    pipeline = joblib.load(model)

    # load category nomenclature into category object
    category = joblib.load(category_path)

    print(category)

    new_doc = []
    with open(doc, mode='r') as in_file:
        for record in in_file:
            # record = remove_hdl.sub('@', record)
            record = remove_tco.sub(' ', record)
            new_doc.append(record.strip())

    # predict the outcome on the testing set and store it in a variable named y_predicted
    y_predicted = pipeline.predict(new_doc)

    harassment = 0
    no_harassment = 0

    for doc, cat in zip(new_doc, y_predicted):
        if cat == 0:
            harassment += 1

        else:
            no_harassment += 1
            print(doc, '-->', category[cat])

    print()
    print('Total number of harassment documents -------> {:>7}'.format('{:,d}'.format(harassment)))
    print('Total number of NO harassment documents ----> {:>7}'.format('{:,d}'.format(no_harassment)))

    return


if __name__ == '__main__':
    """
    :param model_path: path and filename where model resides
    :param cat_path: path and filename for category nomenclature
    :param doc: path and filename where document resides       
    """

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # checks if path was passed as an argument
    if len(sys.argv) != 4:
        print('Usage: python3 Predictor.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    path = sys.argv[1]
    cat_path = sys.argv[2]
    doc_path = sys.argv[3]

    if not os.path.isfile(path):
        print('\nCould not find model in file: %s' % path)
        print('Usage: python3 Predictor.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    if not os.path.isfile(cat_path):
        print('\nCould not find category file: %s' % cat_path)
        print('Usage: python3 Predictor.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    if not os.path.isfile(doc_path):
        print('\nCould not find document: %s' % doc_path)
        print('Usage: python3 Predictor.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    predict(path, cat_path, doc_path)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
