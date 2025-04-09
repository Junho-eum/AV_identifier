from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def click_checkbox(driver):
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='checkbox']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    driver.execute_script("arguments[0].click();", checkbox)


def click_start_button(driver):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        text = btn.text.strip().lower()

        if "start age verification" in text:
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", btn)
            print("🖱️ Clicked button: 'start age verification'")
            return "standard_av"

        elif "enter" in text or "i am 18" in text or "continue" in text:
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", btn)
            print("🖱️ Clicked button: self-declaration (e.g., 'Enter')")
            return "self_declaration"

    return None
