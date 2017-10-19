import sys
import twitter
from time import strftime, localtime, time
from twitter_api.Keys import provide_keys
import twitter_api.Subjects as research
import time as timeit

"""
This Python program
  1. takes as a command line argument twitter handle
  2. extract tweets associated with handle
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Sep 14, 2017 at 13:52:33'
__email__ = 'pvargas@cs.odu.edu'


def tweets(filename, **kwargs):   # handler is twitter user name without @ example phone_dude for @phone_dude
    # keys and tokens from the Twitter Dev Console
    key = provide_keys('males')

    api = twitter.Api(consumer_key=key['consumer_key'],
                      consumer_secret=key['consumer_secret'],
                      access_token_key=key['access_token_key'],
                      access_token_secret=key['access_token_secret'])


    """
    Parameters used in GetHomeTimeline twitter API:
       max_id: initialized to 'None' - Returns results with an ID less than (that is, older than) or
               equal to the specified ID.
       count: Specifies the number of statuses to retrieve. May not be greater than 200.
              Variable max_count is initialized to 200 to get max number of tweets allowed.
    """

    # file where retrieved tweets will reside
    fhs = open(filename, "w")

    handles = research.get_values(**kwargs)
    max_count = 200

    counter = 1
    for account in handles:
        print(account['handle'])

        try:
            timeline_block = api.GetUserTimeline(screen_name=account['handle'],  count=max_count)

            for my_tweets in timeline_block:
                print(counter, my_tweets.text.replace("\n", ' '), my_tweets.created_at, my_tweets.id, len(timeline_block))
                fhs.write('{0}{1}'.format(my_tweets.text.replace("\n", ' '), '\n'))
                counter += 1

            if not timeline_block:
                print('There are no more tweets!!')

        except twitter.error.TwitterError as e:
            print('We have to wait 15 mins.')
            print(e)
            timeit.sleep(61 * 15)

    """
    current_id = None
    max_count = 200
    counter = 1
    no_exception = True
    while no_exception:
        max_id = current_id
        try:
            #timeline_block = api.GetHomeTimeline(count=max_count, max_id=max_id)

            for my_tweets in timeline_block:
                if current_id != my_tweets.id:
                    current_id = my_tweets.id
                    print(counter, my_tweets.text.replace("\n", ' '), my_tweets.created_at, my_tweets.id, len(timeline_block))
                    fhs.write('{0}{1}'.format(my_tweets.text.replace("\n", ' '), '\n'))
                    counter += 1

            if not timeline_block:
                print('There are no more tweets!!')
                no_exception = False

        except twitter.error.TwitterError as e:
            print('We have to wait 15 mins.')
            print(e)
            timeit.sleep(61 * 15)
    """

    fhs.close()

    return


if __name__ == '__main__':
    # checks for argument
    if len(sys.argv) < 2:
        print('Usage: python3 GetTweets.py <filename> <params>')
        sys.exit(-1)

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    param = {}
    for value in sys.argv[2:]:
        print(value)
        param[value.split('=')[0]] = value.split('=')[1]

    outfile = sys.argv[1]

    tweets(outfile, **param)
    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
