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
    message = funFact.get_message()
    # print(message)
    # print("The message is generated")
    # time.sleep(500000)
    post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, message)
