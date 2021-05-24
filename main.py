import tweepy as twitter
import time, datetime
import os
from os import environ

API_KEY = environ['API_KEY']
API_SECRET_KEY = environ['API_SECRET_KEY']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
SECRET_ACCESS_TOKEN = environ['SECRET_ACCESS_TOKEN']

auth = twitter.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
api = twitter.API(auth)

def twitter_bot(hashtag, delay):
    while True:
        print(f"\n{datetime.datetime.now()}\n")

        for tweet in twitter.Cursor(api.search, q=hashtag, rpp='0').items(1):
            try:
                tweet_id = dict(tweet._json)["id"]
                tweet_text = dict(tweet._json)["text"]

                print("id: " + str(tweet_id))
                print("text: " + str(tweet_text))

                api.create_favorite(tweet_id)
                api.retweet(tweet_id)

            except twitter.TweepError as error:
                print(error.reason)

        time.sleep(delay)

twitter_bot("#SFV_saguao", 10)