# twitter-stream1.py

import tweepy
from datetime import timedelta
from urllib3.exceptions import ProtocolError
import sys
import datetime
import blackList
import os
from os import environ

VERSION = 20210603001

CK = environ['API_KEY']
CS = environ['API_SECRET_KEY']
AT = environ['ACCESS_TOKEN']
AS = environ['SECRET_ACCESS_TOKEN']

BLACK_LIST = blackList.BLACK_LIST

def doRetweet(tweetId):
    try:
        api.retweet(tweetId)  # Retweet
    except Exception as e:
        print('------------- Exception -----------------')
        print(e)
        print(datetime.datetime.now())
        sys.stdout.flush()


class Listener(tweepy.StreamListener):  # StreamListenerを継承するクラスListener作成
    def on_status(self, status):
        if status.text.find('RT @') != 0:  # RTされた投稿は対象外 : RTは先頭に RT @NAME が追加される
            status.created_at += timedelta(hours=9)  # 世界標準時から日本時間に
            print('-------------- INFO ----------------')
            print("status.author.name = {author_name}, status.author.screen_name = {author_screen_name}, status.author.id = {status_author_id}, status.created_at = {status_created_at}\n".format(
                author_name=status.author.name, author_screen_name=status.author.screen_name, status_author_id=status.author.id, status_created_at=status.created_at))
            sys.stdout.flush()
            isBlackListUser = status.author.id in BLACK_LIST

            if isBlackListUser:
                print("-------------- Black List User --------------")
                sys.stdout.flush()
            else:
                doRetweet(status.id)

        return True

    def on_error(self, status_code):
        print('Error: ' + str(status_code))
        print(datetime.datetime.now())
        sys.stdout.flush()
        return True

    def on_timeout(self):
        print('Timeout...')
        print(datetime.datetime.now())
        sys.stdout.flush()
        return True


print("ver = {ver} start!!".format(ver=VERSION))
print(datetime.datetime.now())

# Twitter
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

# Listener
listener = Listener()

# 受信開始
stream = tweepy.Stream(auth, listener)

while True:
    try:
        print('-------------- stream.filter ----------------')
        print(datetime.datetime.now())
        sys.stdout.flush()
        stream.filter(track=["#SFV_saguao"])
    except ProtocolError:
        print('-------------- ProtocolError -> continue ----------------')
        print(datetime.datetime.now())
        sys.stdout.flush()
        continue