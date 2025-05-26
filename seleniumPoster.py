from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def post_tweet(username, password, message):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://twitter.com/login")

        # Login sequence
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "text"))
        ).send_keys(username + "\n")
        time.sleep(2)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password + "\n")

        # Wait until home page loads
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Profile"]'))
        )

        # Navigate to tweet composer
        time.sleep(5)  # Wait to stabilize the page load
        editor_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="DraftEditor-editorContainer"]'))
        )
        editor_field.click()

        element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'public-DraftEditorPlaceholder-root')))
        ActionChains(driver).move_to_element(element).send_keys(message).perform()

        sendTw = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]')))
        sendTw.click()

        print("Tweet posted successfully!")
        time.sleep(5)

    except Exception as e:
        print("Error during tweeting:", e)

    finally:
        driver.quit()