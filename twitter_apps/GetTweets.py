import sys
import json
import twitter
from time import strftime, localtime, time
from twitter_apps.Keys import provide_keys
import twitter_apps.Subjects as research
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

    # get all handles from research subject
    handles = research.get_values(**kwargs)
    max_count = 3200
    data = []

    counter = 0
    for account in handles:
        print(account['handle'])

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = retrieve_tweets(api, account['handle'])

        # create initial json_obj for given handle
        json_obj = {'handle': account['handle'], 'tweets': []}

        # add new tweets to created json_oj
        add_tweet_to_handle(json_obj, new_tweets, counter)
        counter += len(new_tweets)

        # save the id of the oldest tweet less one
        if len(new_tweets) > 0:
            oldest = new_tweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = retrieve_tweets(api, account['handle'], max_count,  oldest)

            add_tweet_to_handle(json_obj, new_tweets, counter)
            counter += len(new_tweets)

            # update the id of the oldest tweet less one
            if len(new_tweets) > 0:
                oldest = new_tweets[-1].id - 1

        # save handle tweets
        data.append(json_obj)

    with open(filename, 'w') as out_file:
        json.dump(data, out_file, sort_keys=True, indent=4)

    return


def add_tweet_to_handle(account_obj, tweet_list, counter):
    for my_tweets in tweet_list:
        counter += 1
        print(counter, my_tweets.text.replace("\n", ' '), my_tweets.created_at, my_tweets.id, len(tweet_list))
        account_obj['tweets'].append((my_tweets.text.replace("\n", ' '), my_tweets.created_at))


def retrieve_tweets(api, screen_name, count=200, max_id=None):
    have_to_wait = True

    while have_to_wait:
        try:
            tweet_block = api.GetUserTimeline(screen_name=screen_name, count=count,  max_id=max_id)
            have_to_wait = False
        except twitter.error.TwitterError as e:
            print('We have to wait 15 mins.')
            print(e)
            timeit.sleep(61 * 15)

    return tweet_block


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
