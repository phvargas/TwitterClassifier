import os
import sys
import re
import twitter
import time as timeit
import pickle
import gzip
import json
from twitter_apps.TwitterFunctions import TObject
from Utilities.ProgressBar import display_progress_bar


class TweetClass:
    def __init__(self, path_tweet, auth='male'):
        self.path = path_tweet
        self.handles = []
        self.auth = auth
        self.suffix = '.twt.gz'

        if os.path.isdir(path_tweet):
            self.load_tweets_files()

        else:
            print("Could not find tweet folder: {}".format(path_tweet), file=sys.stderr)
            exit(-1)

        self.handle_with_tweets = len(self.handles)
        self.tweetObject = TObject(self.auth)

    def load_tweets_files(self,):
        dir_files = os.listdir(self.path)
        regex = re.compile('.*\.twt\.gz$')
        tweet_files = sorted([m.group(0) for l in dir_files for m in [regex.search(l)] if m])

        for tweet_file in tweet_files:
            # find where to split filename to obtain handle. Filename format handle_date.html.gz
            value = tweet_file.split('.')
            handle = value[0]

            self.handles.append(handle)
        self.handles.sort()

    def get_tweets(self, handle, max_count=3200):
        if max_count < 200:
            default_count = max_count
        else:
            default_count = 200

        handle_tweets = []
        print("Getting tweets for {}".format(handle), file=sys.stderr)

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.retrieve_tweet_blocks(handle, default_count)
        for tweet in new_tweets:
            handle_tweets.append(tweet)

        oldest = None
        block_size = len(new_tweets)

        # save the id of the oldest tweet less one
        if block_size > 0:
            oldest = new_tweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while 0 < len(handle_tweets) < max_count:
            # all subsequent requests use the max_id param to prevent duplicates
            if max_count == 3200 or (max_count - len(handle_tweets)) > 200:
                default_count = 200
            else:
                default_count = max_count - len(handle_tweets)

            new_tweets = self.retrieve_tweet_blocks(handle, default_count, oldest)

            for tweet in new_tweets:
                handle_tweets.append(tweet)
            display_progress_bar(20, len(handle_tweets)/max_count)

            # update the id of the oldest tweet less one
            if len(new_tweets) > 0:
                oldest = new_tweets[-1].id - 1
            else:
                return handle_tweets

        return handle_tweets

    def retrieve_tweet_blocks(self, screen_name, count=200, max_id=None):
        have_to_wait = True
        tweet_block = []

        while have_to_wait:
            try:
                tweet_block = self.tweetObject.api.GetUserTimeline(screen_name=screen_name, count=count,  max_id=max_id)
                have_to_wait = False
            except twitter.error.TwitterError as e:
                print(screen_name, 'message:', e.message)

                if e.message == 'Not authorized.' or 'Unknown error: ' in e.message or e.message[0]['code'] == 34:
                    print('Account deleted or not authorized... Moving on ... ')
                    return []

                print('Waiting 15 mins.')
                timeit.sleep(61 * 15)

        return tweet_block

    def save(self, handle, _data):
        """
        save objects into a compressed diskfile
        :param
        """
        filename = self.path + handle + self.suffix

        with gzip.open(filename, mode='wb') as f:
            pickle.dump(_data, f, pickle.HIGHEST_PROTOCOL)

    def json_save(self, handle, _data):
        """
        save objects into a compressed diskfile
        :param
        """
        json_str = json.dumps(_data) + "\n"
        json_bytes = json_str.encode('utf-8')

        filename = self.path + handle + self.suffix

        with gzip.open(filename, mode='wb') as f:
            f.write(json_bytes)

    def load(self, handle):
        """
        reload objects from a compressed diskfile
        """
        filename = self.path + handle + self.suffix

        with gzip.open(filename, mode='rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = pickle.load(f)

        return data
