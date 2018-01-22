import sys
import os
import re
from time import strftime, localtime, time
from Utilities.CleanDoc import clean_doc
from Utilities.Sorting import dictionaryByValue
from sklearn.feature_extraction import text


"""
    Given a set of files containing tweets from identified harasser Twitter account:
       1. identified deleted/suspended/private accounts
       2.      
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  Jan 19, 2018 at 10:51'
__email__ = 'pvargas@cs.odu.edu'


stop_words = text.ENGLISH_STOP_WORDS.union(['https', 'http', 'rt', '@hdl', '&amp'])


def get_BOWD(in_file):
    word_count = {}
    accounts = get_tweets(in_file)
    for tweets in accounts:
        print('<<{}>>'.format(tweets))
        for tweet in accounts[tweets]:
            word_count = get_word_count(word_count, tweet.split())
            print('\t{}'.format(tweet))

    fhs = open('harssers-zipt.dat', mode='w')
    fhs.write('word\tvalue\n')

    for freq, value in dictionaryByValue(word_count):
        print(freq, value)
        fhs.write('{}\t{}\n'.format(freq, value))
    fhs.close()

    print(stop_words)
    return


def get_word_count(obj, vector):
    for word in vector:
        if word not in stop_words and word not in obj:
            obj[word] = 1
        elif word not in stop_words:
            obj[word] += 1

    return obj


def get_tweets(in_file):
    """
    :param in_file: file containing extracted tweets from harassers timeline
    :return: void
    """
    regex = re.compile("(<<)(\\S+)(>>)")
    counter = 0
    accounts = {}

    # iterate throughout the entire file
    with open(in_file, mode='r') as fhs:
        for record in fhs:
            record = record.strip()
            is_handle = regex.match(record)

            # record read is handle's name
            if is_handle:
                counter += 1
                current_handle = is_handle.group(2)
                accounts[current_handle] = []

            # append tweet to current handle
            elif record:
                accounts[current_handle].append(clean_doc(record))
                # accounts[current_handle].append(record)

            # empty value for handle
            else:
                pass
    return accounts


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
        sys.exit(-1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print('\nCould not find file: %s' % filename)
        print('Usage: python3 ReadHarassersTweets.py <path>')
        sys.exit(-1)

    get_BOWD(filename)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
