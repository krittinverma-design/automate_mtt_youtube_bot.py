import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# YouTube channel link
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel/UC0_POCFlmtlMG-KkRPP_oAg"

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-breakpad")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")
    options.add_argument("--no-first-run")
    options.add_argument("--no-service-autorun")
    options.add_argument("--password-store=basic")
    options.add_argument("--use-mock-keychain")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver):
    driver.get("https://mytoolstown.com/youtube")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='channel']")))
    channel_input = driver.find_element(By.CSS_SELECTOR, "input[name='channel']")
    channel_input.clear()
    channel_input.send_keys(YOUTUBE_CHANNEL_URL)
    channel_input.send_keys(Keys.RETURN)

def earn_credits(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".task-button")))
    task_buttons = driver.find_elements(By.CSS_SELECTOR, ".task-button")
    for button in task_buttons:
        try:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)  # Adjust sleep time as necessary
        except Exception as e:
            print(f"Error clicking task button: {e}")

def main():
    driver = setup_driver()
    try:
        login(driver)
        earn_credits(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
