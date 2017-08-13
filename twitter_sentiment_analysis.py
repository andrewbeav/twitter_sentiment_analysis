import tweepy
from textblob import TextBlob
import sys
import configparser

config = configparser.ConfigParser()

try:
	config.readfp(open('config.txt'))
except FileNotFoundError:
	print('No configuration file. Create config.txt')

# Setting up authentication
consumer_key = config.get('twitter', 'consumer_key')
consumer_secret = config.get('twitter', 'consumer_secret')

access_token = config.get('twitter', 'access_token')
access_token_secret = config.get('twitter', 'access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up tweepy api
api = tweepy.API(auth)

keyword = sys.argv[1]
tweets = api.search(keyword)

tweet_sentiment_polaritys = []
for tweet in tweets:
	tweet_sentiment_polaritys.append(TextBlob(tweet.text).sentiment.polarity)

avg = sum(tweet_sentiment_polaritys)/len(tweet_sentiment_polaritys)
emotion = ''
if avg > 0.1:
	emotion = 'postive'
elif avg < -0.1:
	emotion = 'negative'
else:
	emotion = 'neutral'

print('In general, people on twitter feel {} about {} right now'.format(emotion, keyword))
