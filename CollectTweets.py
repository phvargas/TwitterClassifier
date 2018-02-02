import sys
import os
import pickle
from time import strftime, localtime, time
from twitter_apps.TwitterFunctions import TObject
from twitter_apps.GetTweets import retrieve_tweets


"""
    Given a set of set of Twitter handles get n number of tweets.     
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Thr, Fec 01 2018 at 17:03'
__email__ = 'pvargas@cs.odu.edu'


def get_tweets(in_file, output_file, max_count):
    """
    :param in_file: pickle file containing twitter handle
    :param output_file: output file containing max tweets allowed for ids in input file
    :param max_count: number of tweets to collect. Max allowed by Twitter is 3200
    :return: void
    """
    pkl_file = open(in_file, 'rb')
    followers_id = pickle.load(pkl_file)
    pkl_file.close()

    for value in followers_id:
        print(value, followers_id[value])
        break

    sys.exit(0)

    tObj = TObject()

    counter = 0
    out_fhs = open(output_file, mode='w')
    for account in followers_id:
        print(account)

        out_fhs.write('<<{}>>\n'.format(account))

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = retrieve_tweets(tObj.api, account)

        # add new tweets to created json_oj
        counter += len(new_tweets)
        account_tweet_count = len(new_tweets)

        for my_tweets in new_tweets:
            counter += 1
            print(counter, my_tweets.text.replace("\n", ' '), my_tweets.created_at, my_tweets.id, len(new_tweets))
            out_fhs.write('{}\n'.format(my_tweets.text.replace("\n", ' ')))

        # save the id of the oldest tweet less one
        if len(new_tweets) > 0:
            oldest = new_tweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0 and account_tweet_count < max_count:
            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = retrieve_tweets(tObj.api, account, max_count,  oldest)

            counter += len(new_tweets)
            account_tweet_count += len(new_tweets)

            # update the id of the oldest tweet less one
            if len(new_tweets) > 0:
                oldest = new_tweets[-1].id - 1

            for my_tweets in new_tweets:
                counter += 1
                print(counter, my_tweets.text.replace("\n", ' '), my_tweets.created_at, my_tweets.id, len(new_tweets))
                out_fhs.write('{}\n'.format(my_tweets.text.replace("\n", ' ')))

        print()
        out_fhs.write('\n')

    out_fhs.close()

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
    if len(sys.argv) < 4:
        print('Usage: python3 HarasserTweets.py <input_file> <output_file> <max_count>')
        sys.exit(-1)

    input_file = sys.argv[1]
    out_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print('\nCould not file: %s' % input_file)
        print('Usage: python3 HarasserTweets.py <input_file> <output_file> <max_count>')
        sys.exit(-1)

    if not sys.argv[3].isdigit():
        print('\nMax_Count: %s must be an integer' % sys.argv[3])
        print('Usage: python3 HarasserTweets.py <input_file> <output_file> <max_count>')
        sys.exit(-1)

    get_tweets(input_file, out_file, sys.argv[3])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
