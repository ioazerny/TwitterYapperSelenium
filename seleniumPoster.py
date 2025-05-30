from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from pathlib import Path
import cv2
import pyautogui
from selenium.common.exceptions import TimeoutException

def post_tweet(username, password, message):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://twitter.com/login")

        # Login sequence (optimized)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "text"))
        ).send_keys(username + "\n")
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password + "\n")

        # Wait for home page using presence rather than profile element
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]'))
        )

        # Optimized compose section
        editor = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]'))
        )
        editor.click()
        ActionChains(driver).send_keys(message).perform()

        # Streamlined post strategies (keep 3 most reliable)
        post_strategies = [
            # Primary selector (data-testid)
            lambda: driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']").click(),
            
            # JavaScript fallback
            lambda: driver.execute_script(
                "document.querySelector('[data-testid=\"tweetButtonInline\"]').click();"
            ),
            
            # Text-based fallback
            lambda: driver.find_element(By.XPATH, "//span[contains(text(), 'Post')]/ancestor::div[@role='button']").click()
        ]

        for strategy in post_strategies:
            try:
                strategy()
                print("Tweet posted successfully!")
                time.sleep(2)  # Minimal wait for confirmation
                break
            except Exception as e:
                continue
        else:
            print("All strategies failed")

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()
