from credentials import *
from weather import get_weather
from trumpSummarizer import get_trump_summary
from authorsNote import get_authors_note
import tweepy

def post_tweet(content: str):
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )
    response = client.create_tweet(text=content)
    print(f"Tweet posted: {content}")
    return response

def post_weather_tweet():
    tweet = get_weather()
    return post_tweet(tweet)

def post_trump_tweet():
    tweet = get_trump_summary()
    return post_tweet(tweet)

def post_authors_note_tweet():
    tweet = get_authors_note()
    return post_tweet(tweet)
