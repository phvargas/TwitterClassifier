import sys
import os
import json
import twitter_apps.Subjects as research
from twitter_apps.Sentiment import TwitterClient
from time import strftime, localtime, time

"""
This Python program
  1. Inspect data set used for Twitter Harassment
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Sep 22, 2017 at 18:28:30'
__email__ = 'pvargas@cs.odu.edu'


def print_number_tweets(filename):
    accounts = {}
    for account in research.get_values():
        accounts[account['handle']] = account

    with open(filename, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    counter = 0
    for account in data:
        print('{0},{1},{2}'.format(accounts[account['handle']]['handle'],
                                   accounts[account['handle']]['name'],
                                   len(account['tweets'])))
        counter += len(account['tweets'])

    print()
    print('Total number of tweets:', counter)

    return


def print_account_sentiment(filename):
    accounts = {}
    for account in research.get_values():
        accounts[account['handle']] = account

    with open(filename, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    api = TwitterClient()

    for account in data:
        tweets = []
        for tweet in account['tweets']:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}

            parsed_tweet['sentiment'] = api.get_tweet_sentiment(tweet[0])

            tweets.append(parsed_tweet)

        total_tweets = len(tweets)

        if total_tweets:
            # picking positive tweets from tweets
            ptweets = len([tweet for tweet in tweets if tweet['sentiment'] == 'positive']) / total_tweets * 100
            ptweets = round(ptweets, 2)

            # picking negative tweets from tweets
            ntweets = len([tweet for tweet in tweets if tweet['sentiment'] == 'negative']) / total_tweets * 100
            ntweets = round(ntweets, 2)

            neutral = 100 - ntweets - ptweets

        else:
            ptweets = 0
            ntweets = 0
            neutral = 0

        print('{0},{1},{2:.2f}'.format(accounts[account['handle']]['name'], 'positive', ptweets))
        print('{0},{1},{2:.2f}'.format(accounts[account['handle']]['name'], 'negative', ntweets))
        print('{0},{1},{2:.2f}'.format(accounts[account['handle']]['name'], 'neutral', neutral))

    return


if __name__ == '__main__':
    # checks for argument
    if len(sys.argv) < 2:
        print('Usage: python3 InspectSubjects.py <filename>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('Could not find input file: %s' % sys.argv[2])
        print('Usage: python3 InspectSubjects.py <filename>')
        sys.exit(-1)

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    print_number_tweets(sys.argv[1])

    print()
    print()
    print_account_sentiment(sys.argv[1])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
