import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import json

consumer_key = 'consumer_key_here'
consumer_secret = 'consumer_secret_here'
access_token = 'access_token_here'
access_secret = 'access_secret_here'

auth = OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
auth.set_access_token(access_token, access_secret)

#search
api = tweepy.API(auth)
# test = api.lookup_users(user_ids=['3022906249'])
test = api.lookup_users(screen_names=['Tearfund'])

# print test
for user in test:
    print user.id
    print user.screen_name
    print user.name
    print user.description
    print user.location
    # print user.followers_count
    # print user.statuses_count
    # print user.url