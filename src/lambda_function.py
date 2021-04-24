import os
import random
import json
from pathlib import Path
import tweepy
import csv
import markovify
import nltk
import re

dirname = os.path.dirname(os.path.abspath(__file__))
tweets = os.path.join(dirname, 'tweets.txt')

with open(tweets) as f:
    text = f.read()

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


text_model = markovify.Text(text)


ROOT = Path(__file__).resolve().parents[0]


def get_tweet():
    return text_model.make_short_sentence(280)


def lambda_handler(event, context):
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("Markovify a tweet")
    tweet = get_tweet()

    print(f"Post tweet: {tweet}")
    api.update_status(tweet)

    return {"statusCode": 200, "tweet": tweet}
