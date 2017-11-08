import tweepy
from twitter_apps.Keys import provide_keys

# keys and tokens from the Twitter Dev Console
key = provide_keys('males')

# Consumer keys and access tokens, used for OAuth
consumer_key = key['consumer_key']
consumer_secret = key['consumer_secret']
access_token = key['access_token_key']
access_token_secret = key['access_token_secret']

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

print(api.me().name)

counter = 0
for status in tweepy.Cursor(api.home_timeline, screen_name='@MalePHV', since_id=918830457550262272).items():
    counter += 1
    print('<{0}>   {1}   <{2}> '.format(counter, status._json['text'], status.id))
