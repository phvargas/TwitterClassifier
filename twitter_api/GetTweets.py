import sys
import twitter
from time import strftime, localtime, time
from twitter_api.Keys import provide_keys
import time as timeit

"""
This Python program
  1. takes as a command line argument twitter handle
  2. extract tweets associated with handle
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Sep 14, 2017 at 13:52:33'
__email__ = 'pvargas@cs.odu.edu'


def tweets(handler):   # handler is twitter user name without @ example phone_dude for @phone_dude
    # keys and tokens from the Twitter Dev Console
    key = provide_keys('males')

    api = twitter.Api(consumer_key=key['consumer_key'],
                      consumer_secret=key['consumer_secret'],
                      access_token_key=key['access_token_key'],
                      access_token_secret=key['access_token_secret'])

    user = api.GetUser(screen_name=handler)
    fhs = open("test.txt", "a")

    """
    Parameters used in GetHomeTimeline twitter API:
       max_id: initialized to 'None' - Returns results with an ID less than (that is, older than) or
               equal to the specified ID.
       count: Specifies the number of statuses to retrieve. May not be greater than 200.
              Variable max_count is initialized to 200 to get max number of tweets allowed.
    """
    current_id = '917942719061913601'
    max_count = 200
    counter = 1
    no_exception = True
    while no_exception:
        max_id = current_id
        try:
            #timeline_block = api.GetUserTimeline(user_id=user.id,  count=max_count, max_id=max_id)
            timeline_block = api.GetHomeTimeline(count=max_count, max_id=max_id)

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

    fhs.close()
    print(handler)

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
    tweets(sys.argv[1])
    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
