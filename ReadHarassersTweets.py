import sys
import os
import re
import gzip
from time import strftime, localtime, time


"""
    Given a set of set of ids get max number of tweets.     
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  Dec 13, 2017 at 10:51'
__email__ = 'pvargas@cs.odu.edu'


def get_tweets(in_file):
    """
    :param in_file: file containing extracted tweets from harassers timeline
    :return: void
    """
    regex = re.compile("(<<)(\\S+)(>>)")
    counter = 0
    deleted_accounts = 0
    bad_accounts = []
    with gzip.open(in_file, mode='r') as fhs:
        for record in fhs:
            record = record.strip().decode('utf-8')
            is_handle = regex.match(record)
            if is_handle:
                counter += 1
                current_handle = is_handle.group(2)
                handle_tweets = []

            elif record:
                handle_tweets.append(record)
            else:
                if len(handle_tweets) == 0:
                    print(counter, current_handle, len(handle_tweets), handle_tweets)
                    deleted_accounts += 1
                    bad_accounts.append(current_handle)

    print('\nNumber of harassers: {}'.format(counter))
    print('\nNumber of deleted accounts: {}'.format(deleted_accounts))
    print(bad_accounts)

    return


if __name__ == '__main__':
    """
    :param input_file: file containing extracted tweets from harassers timeline    
    """

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # checks if path was passed as an argument
    if len(sys.argv) < 2:
        print('Usage: python3 ReadHarassersTweets.py <input_file>')
        sys.exit(-1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print('\nCould not file: %s' % input_file)
        print('Usage: python3 ReadHarassersTweets.py <input_file>')
        sys.exit(-1)

    get_tweets(input_file)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
