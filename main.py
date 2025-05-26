from seleniumPoster import post_tweet
import authorsNote
from credentials import TWITTER_USERNAME, TWITTER_PASSWORD

if __name__ == "__main__":
    message = authorsNote.get_authors_note()
    post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, message)
