from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def post_tweet(username, password, message):
    driver = webdriver.Chrome()  # assumes chromedriver is installed
    driver.get("https://twitter.com/login")
    time.sleep(3)

    # Username
    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # Password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Tweet box
    tweet_box = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Tweet text']")
    tweet_box.click()
    tweet_box.send_keys(message)

    # Tweet button
    tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
    tweet_button.click()
    print("✅ Tweet sent!")

    time.sleep(2)
    driver.quit()
