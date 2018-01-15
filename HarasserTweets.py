import sys
import os
import pickle
from time import strftime, localtime, time
from twitter_apps.TwitterFunctions import TwitterObject
from twitter_apps.GetTweets import retrieve_tweets


"""
    Given a set of set of ids get max number of tweets.     
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  Dec 13, 2017 at 10:51'
__email__ = 'pvargas@cs.odu.edu'


def get_tweets(in_file, output_file):
    """
    :param in_file: pickle file containing twitter handle
    :param output_file: output file containing max tweets allowed for ids in input file
    :return: void
    """
    pkl_file = open(in_file, 'rb')
    followers_id = pickle.load(pkl_file)
    pkl_file.close()

    tObj = TwitterObject()

    for account in followers_id:
        tweets = retrieve_tweets(tObj.api, account)
        print(tweets)

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
    if len(sys.argv) != 3:
        print('Usage: python3 HarasserTweets.py <input_file> <output_file>')
        sys.exit(-1)

    input_file = sys.argv[1]
    out_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print('\nCould not find model in file: %s' % input_file)
        print('Usage: python3 HarasserTweets.py <input_file> <output_file>')
        sys.exit(-1)

    get_tweets(input_file, out_file)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
