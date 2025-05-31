from seleniumPoster import post_tweet
import authorsNote
import weather
import trumpSummarizer
import funFact
from credentials import TWITTER_USERNAME, TWITTER_PASSWORD
import random
import time

if __name__ == "__main__":
     options = [weather, trumpSummarizer, authorsNote, funFact]
#    message = random.choice(options).get_message()
#    post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, message)
