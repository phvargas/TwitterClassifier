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


def inspect_all_files(folder_path):
    vector_file = [
        'HarasserTweets.20171219.gz',
        'HarasserTweets.20171227.gz',
        'HarasserTweets.20180104.gz',
        'HarasserTweets.20180110.gz',
        'HarasserTweets.20180113.gz',
        'HarasserTweets.20180117.gz'
    ]

    vector_set = []

    for filename in vector_file:
        filename = folder_path + '/' + filename
        if not os.path.isfile(filename):
            print('\nCould not find file: %s' % filename)
            print('inspecting next file....')
            break

        vector_set.append(set(get_tweets(filename)))

    for vector in vector_set:
        print(len(vector), vector)

    final_set = list(vector_set[-1] - vector_set[0])
    tweets = get_handle_tweets(folder_path + "/" + vector_file[0], final_set)

    for account in tweets:
        print('<<{}>>'.format(account))
        for tweet in tweets[account][:50]:
            print('\t{}'.format(tweet))
        print()

    print(vector_set[-1])
    print(vector_set[0])
    print(list(vector_set[-1] - vector_set[0]))
    return


def get_handle_tweets(in_file, handle_list):
    regex = re.compile("(<<)(\\S+)(>>)")
    valid_handle = False
    handle = {}

    # iterate throughout the entire file
    with gzip.open(in_file, mode='r') as fhs:
        for record in fhs:
            record = record.strip().decode('utf-8')
            is_handle = regex.match(record)

            # record read is handle's name
            if is_handle:
                current_handle = is_handle.group(2)
                if current_handle in handle_list:
                    valid_handle = True
                    handle[current_handle] = []
                else:
                    valid_handle = False

            # append tweet to current handle
            elif record:
                if valid_handle:
                    handle[current_handle].append(record)

            # empty value for handle
            else:
                pass

    return handle


def get_tweets(in_file):
    """
    :param in_file: file containing extracted tweets from harassers timeline
    :return: void
    """
    regex = re.compile("(<<)(\\S+)(>>)")
    counter = 0
    deleted_accounts = 0
    bad_accounts = []

    # iterate throughout the entire file
    with gzip.open(in_file, mode='r') as fhs:
        for record in fhs:
            record = record.strip().decode('utf-8')
            is_handle = regex.match(record)

            # record read is handle's name
            if is_handle:
                counter += 1
                current_handle = is_handle.group(2)
                handle_tweets = []

            # append tweet to current handle
            elif record:
                handle_tweets.append(record)

            # empty value for handle
            else:
                if len(handle_tweets) == 0:
                    print(counter, current_handle, len(handle_tweets), handle_tweets)
                    deleted_accounts += 1
                    bad_accounts.append(current_handle)

    print('\nNumber of harassers: {}'.format(counter))
    print('\nNumber of deleted accounts: {}'.format(deleted_accounts))
    print(bad_accounts)

    return bad_accounts


if __name__ == '__main__':
    """
    :param input_file: file containing extracted tweets from harassers timeline    
    """

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 2:
        print('\nProvide path of inspected files...')
        print('Usage: python3 ReadHarassersTweets.py <path>')

    path = sys.argv[1]

    if not os.path.isdir(path):
        print('\nCould not find folder: %s' % path)
        print('Usage: python3 ReadHarassersTweets.py <path>')
        sys.exit(-1)

    inspect_all_files(path)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
