import re
import sys
import os
import tweepy
import json
from tweepy import OAuthHandler
from textblob import TextBlob
from time import strftime, localtime, time
from twitter_api.Keys import provide_keys
import twitter_api.Subjects as research


class TwitterClient(object):
    """
    Generic Twitter Class for sentiment analysis.
    """

    def __init__(self):
        """
        Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        key = provide_keys('males')

        consumer_key = key['consumer_key']
        consumer_secret = key['consumer_secret']
        access_token = key['access_token_key']
        access_token_secret = key['access_token_secret']

        # attempt authentication

        # create OAuthHandler object
        self.auth = OAuthHandler(consumer_key, consumer_secret)

        # set access token and secret
        self.auth.set_access_token(access_token, access_token_secret)

        try:
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")
            sys.exit(-1)

    def clean_tweet(self, tweet):
        """
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w +://\S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        """
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        """
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))

        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        """
        Main function to fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    def get_tweets_from_file(self, filename):
        """
        Main function to fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []
        if not os.path.isfile(filename):
            print('Could not find file: ', filename)
            return -1

        with open(filename, mode='r', encoding='utf-8') as f:
            # parsing tweets one by one
            for tweet in f:
                print(tweet.strip())
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.strip()
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.strip())

                tweets.append(parsed_tweet)

        # return parsed tweets
        return tweets

    def get_tweets_from_json_file(self, filename, **kwargs):
        """
        Main function to fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []
        if not os.path.isfile(filename):
            print('Could not find file: ', filename)
            return -1

        # get all handles from research subject
        handles = []
        for record in research.get_values(**kwargs):
            handles.append(record['handle'])

        with open(filename, mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

            # parsing tweets one by one
            for account in data:
                print(account)
                if account['handle'] in handles:
                    for record in account['tweets']:
                        tweet = record[0].strip()
                        timestamp = record[1]
                        print(tweet)

                        # empty dictionary to store required params of a tweet
                        parsed_tweet = {}

                        # saving text of tweet
                        parsed_tweet['text'] = tweet.strip()
                        # saving sentiment of tweet
                        parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.strip())

                        tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets


def main(filename, **kwargs):
    # creating object of TwitterClient Class
    api = TwitterClient()

    """
    # calling function to get tweets
    try:
        tweets = api.get_tweets(query='Donald Trump', count=200)

    except tweepy.TweepError as e:
        # print error (if any)
        print("Error : " + str(e))
    """
    # calling function to get tweets
    tweets = api.get_tweets_from_json_file(filename, **kwargs)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    # percentage of positive tweets
    positive_tweets_perc = 100 * len(ptweets) / len(tweets)

    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    # percentage of negative tweets
    negative_tweets_perc = 100 * len(ntweets) / len(tweets)

    # picking negative tweets from tweets
    neutral_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

    neutral_tweets_perc = 100 - positive_tweets_perc - negative_tweets_perc

    # printing first 10 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 10 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    # printing first 10 negative tweets
    print("\n\nNeutral tweets:")
    for tweet in neutral_tweets[:10]:
        print(tweet['text'])

    print()
    print()
    print("Positive tweets percentage: {0} %  total: {1}".format(positive_tweets_perc, len(ptweets)))
    print("Negative tweets percentage: {0} %   total: {1}".format(negative_tweets_perc, len(ntweets)))

    # percentage of neutral tweets
    print("Neutral tweets percentage: {0} %   total: {1}".format(neutral_tweets_perc,
                                                                 len(tweets) - len(ptweets) - len(ntweets)))
    print('Total tweets: ', len(tweets))

    print('{0},{1},{2:.2f},{3}'.format('positive', 'criteria', positive_tweets_perc, len(ptweets)))
    print('{0},{1},{2:.2f},{3}'.format('negative', 'criteria', negative_tweets_perc, len(ntweets)))
    print('{0},{1},{2:.2f},{3}'.format('neutral', 'criteria', neutral_tweets_perc, len(neutral_tweets)))


if __name__ == "__main__":
    # calling main function
    # checks for argument
    if len(sys.argv) < 2:
        print('Usage: python3 Sentiment.py <filename> <params>')
        sys.exit(-1)

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    param = {}
    for value in sys.argv[2:]:
        print(value)
        param[value.split('=')[0]] = value.split('=')[1]

    infile = sys.argv[1]
    main(infile, **param)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
