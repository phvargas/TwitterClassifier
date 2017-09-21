import sys
from time import strftime, localtime, time

"""
This Python program
  1. takes as a command line argument twitter handle
  2. extract tweets associated with handle
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Sep 21, 2017 at 09:46:01'
__email__ = 'pvargas@cs.odu.edu'


def classifier(filename):   #

    return

if __name__ == '__main__':
    # checks for argument
    if len(sys.argv) != 2:
        print('Usage: python3 GetTweets.py <twitter-handle>')
        sys.exit(-1)

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # call extract_tweets
    crawled_pages = {}
    classifier(sys.argv[1])
    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
