import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Your YouTube channel ID for My Tools Town
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel/UC0_POCFlmtlMG-KkRPP_oAg"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def go_to_youtube_section(driver):
    driver.get("https://mytoolstown.com/youtube")  # My Tools Town YouTube section URL
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".task-button")))
    print("[+] YouTube tasks page loaded")

def complete_tasks(driver, max_tasks=5):
    tasks_done = 0
    task_buttons = driver.find_elements(By.CSS_SELECTOR, ".task-button")
    
    for task in task_buttons:
        if tasks_done >= max_tasks:
            break

        try:
            # Skip task if already marked completed (you may need to adjust selector)
            if "completed" in task.get_attribute("class").lower():
                print("[~] Task already completed, skipping")
                continue

            driver.execute_script("arguments[0].scrollIntoView(true);", task)

            # Paste YouTube channel URL if required
            try:
                input_box = task.find_element(By.CSS_SELECTOR, "input[type='text']")
                input_box.clear()
                input_box.send_keys(YOUTUBE_CHANNEL_URL)
            except:
                print("[~] No input box found, continuing")

            task.click()
            print(f"[+] Task {tasks_done+1} completed")

            wait_time = random.randint(5, 10)
            time.sleep(wait_time)

            tasks_done += 1
            time.sleep(random.randint(2, 5))

        except Exception as e:
            print("[!] Error performing task:", e)
            continue

def main():
    driver = setup_driver()
    try:
        go_to_youtube_section(driver)
        complete_tasks(driver, max_tasks=5)  # Adjust max_tasks per run
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
