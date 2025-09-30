import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = os.environ.get("MTT_USERNAME")
PASSWORD = os.environ.get("MTT_PASSWORD")

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login(driver):
    driver.get("https://mytoolstown.com/login")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    WebDriverWait(driver, 20).until(EC.url_contains("dashboard"))
    print("[+] Logged in successfully")

def navigate_to_youtube(driver):
    driver.get("https://mytoolstown.com/youtube")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".task-button")))
    print("[+] YouTube tasks page loaded")

def complete_tasks(driver, max_tasks=5):
    tasks_done = 0
    while tasks_done < max_tasks:
        try:
            task_buttons = driver.find_elements(By.CSS_SELECTOR, ".task-button")
            if not task_buttons:
                print("[!] No more tasks found")
                break

            task = task_buttons[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", task)
            task.click()
            print(f"[+] Task {tasks_done+1} clicked")

            wait_time = random.randint(20, 35)
            print(f"[~] Waiting {wait_time} seconds to mimic watch time...")
            time.sleep(wait_time)

            try:
                confirm = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".confirm-button"))
                )
                confirm.click()
                print(f"[+] Credits claimed for task {tasks_done+1}")
            except:
                print("[!] Could not find confirm button (maybe auto-credited)")

            tasks_done += 1
            time.sleep(random.randint(5, 10))

        except Exception as e:
            print("[!] Error performing task:", e)
            break

def main():
    driver = setup_driver()
    try:
        login(driver)
        navigate_to_youtube(driver)
        complete_tasks(driver, max_tasks=5)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
