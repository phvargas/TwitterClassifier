import sys
import os
import re
import pickle
from time import strftime, localtime, time
from sklearn.externals import joblib
from twitter_apps.TwitterFunctions import TwitterObject


"""
    Given a set of documents contained in a file classified the documents based on a provided persistent model.     
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  Oct 16, 2017 at 13:44:27'
__email__ = 'pvargas@cs.odu.edu'


def predict(model, category_path, doc, outfile, re_start=True, idxfile=0, infile='ConversationHarassment.dat'):
    """
    :param model: folder where dataset classification sub-folders reside
    :param category_path: path where category model resides
    :param doc: path of document to be compared
    :return: void
    """
    remove_tco = re.compile('https?:\\?\s?/\\?\s?/t.co\\?\s?/\S+')
    regex = re.compile('(\\S+)\\s+(\\d+)\\s+(.*)')
    remove_hdl = re.compile('@\S+')

    print('Dictionary will be written on file:', outfile)

    # load model into pipeline object
    pipeline = joblib.load(model)

    # load category nomenclature into category object
    category = joblib.load(category_path)

    print(category)

    new_doc = []
    tweet_id = []
    tweet_hdl = []
    bad_records = 0
    followers_id = {}
    bad_tweets = TwitterObject()

    harassment = 0
    no_harassment = 0

    if re_start.lower() == 'true':
        print('I am passing by')
        # get all conversation tweets
        with open(doc, mode='r') as in_file:
            for record in in_file:
                try:
                    match = regex.match(record.strip())
                    doc = match.group(3)
                    # record = remove_hdl.sub('@', record)
                    doc = remove_tco.sub(' ', doc)

                    new_doc.append(doc)
                    tweet_id.append(match.group(2))
                    tweet_hdl.append(match.group(1))

                except AttributeError:
                    print('Record: {} not valid'.format(record))
                    bad_records += 1

        # predict the outcome on the testing set and store it in a variable named y_predicted
        y_predicted = pipeline.predict(new_doc)

        # write all harassing documents
        with open(infile, mode='w') as out_fhd:
            for handle, idx, doc, cat in zip(tweet_hdl, tweet_id, new_doc, y_predicted):
                if not cat:
                    out_fhd.write('{}\t{}\t{}\n'.format(handle, idx, doc))
    else:
        # read all harassing document
        with open(infile, mode='r') as in_fhd:
            for record in in_fhd:
                match = regex.match(record.strip())
                doc = match.group(3)

                new_doc.append(doc)
                tweet_id.append(match.group(2))
                tweet_hdl.append(match.group(1))

        if idxfile > 0:
            # get follower_id object from pickle
            pkl_file = open(outfile + '.pkl', 'rb')
            followers_id = pickle.load(pkl_file)
            pkl_file.close()

        counter = idxfile
        for handle, idx, doc in zip(tweet_hdl[idxfile:], tweet_id[idxfile:], new_doc[idxfile:]):
            # add user_id to list of harassers
            if handle not in followers_id:
                followers = bad_tweets.get_friends(handle)
                followers_id[handle] = {'followers': followers, 'tweets_id': [idx]}

            else:
                followers_id[handle]['tweets_id'].append(idx)

            output = open(outfile + '.pkl', 'wb')
            pickle.dump(followers_id, output)
            output.close()

            print(counter, '-->', doc, 'handle=', handle, 'friends=', followers_id[handle]['followers'])
            counter += 1

    print()
    # print('Total number of harassment documents -------> {:>7}'.format('{:,d}'.format(harassment)))
    # print('Total number of NO harassment documents ----> {:>7}'.format('{:,d}'.format(no_harassment)))
    print('Total number of bad records ----------------> {:>7}'.format('{:,d}'.format(bad_records)))
    print('Total number of user_ids harassing ---------> {:>7}'.format('{:,d}'.format(len(followers_id))))

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
    if len(sys.argv) != 6:
        print('Usage: python3 ConvUserFilter.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    path = sys.argv[1]
    cat_path = sys.argv[2]
    doc_path = sys.argv[3]

    if not os.path.isfile(path):
        print('\nCould not find model in file: %s' % path)
        print('Usage: python3 ConvUserFilter.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    if not os.path.isfile(cat_path):
        print('\nCould not find category file: %s' % cat_path)
        print('Usage: python3 ConvUserFilter.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    if not os.path.isfile(doc_path):
        print('\nCould not find document: %s' % doc_path)
        print('Usage: python3 ConvUserFilter.py <model_path> <cat_path> <doc_path>')
        sys.exit(-1)

    predict(path, cat_path, doc_path, sys.argv[4], sys.argv[5])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
