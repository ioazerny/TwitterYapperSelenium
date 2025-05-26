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


        # TEMPLATE_MATCHING_IMPLEMENTATION
        project_root = Path.cwd()

        # Create subfolder for organization
        target_dir = project_root / "screenshots"
        target_dir.mkdir(exist_ok=True)

        # Save the screenshot there
        sc_path = target_dir / "screenshot.png"
        driver.save_screenshot(str(sc_path))
        
        # Load the screenshot for processing
        screenshot = cv2.imread(str(sc_path))
        template = cv2.imread("PostButton.png")

        # Match the template to the screenshot
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Set a matching confidence threshold
        threshold = 0.9
        if max_val >= threshold:
            print("Button match found!")

            # Get center of the matched region
            t_height, t_width = template.shape[:2]
            center_x = max_loc[0] + t_width // 2
            center_y = max_loc[1] + t_height // 2
        else:
            raise Exception("Button not found — try adjusting the image or threshold")

        # Scroll to the vertical position of the match (optional)
        driver.execute_script("window.scrollTo(0, arguments[0]);", center_y - 300)

        # Click using offset from top-left of browser window
        actions = ActionChains(driver)
        actions.move_by_offset(center_x, center_y).click().perform()

        # Reset offset to avoid future mis-clicks
        actions.move_by_offset(-center_x, -center_y).perform()




        print("Tweet posted successfully!")
        time.sleep(5)

    except Exception as e:
        print("Error during tweeting:", e)

    finally:
        driver.quit()