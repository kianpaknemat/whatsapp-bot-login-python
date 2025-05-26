from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_with_phone_number(phone_number):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 180)

    try:
        driver.get("https://web.whatsapp.com/")

        # Click "Log in with phone number" button
        login_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(),'Log in with phone number')]")
        ))
        login_btn.click()

        # Skip country selector part (do NOT click or change country)

        # Input phone number field
        phone_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[aria-label='Type your phone number.']")
        ))

        # Method 1: More thorough clearing
        phone_input.click()
        phone_input.clear()
        time.sleep(0.5)  # Small delay

        # Select all and delete to ensure complete clearing
        phone_input.send_keys(Keys.CONTROL + "a")
        phone_input.send_keys(Keys.DELETE)
        time.sleep(0.5)

        # Now send the complete phone number
        full_number = f"+98{phone_number}"
        phone_input.send_keys(full_number)

        # Alternative Method 2: Character by character input (uncomment if above doesn't work)
        # for char in full_number:
        #     phone_input.send_keys(char)
        #     time.sleep(0.1)

        # Wait a moment for any auto-formatting to complete
        time.sleep(1)

        # Verify the input value
        current_value = phone_input.get_attribute("value")
        print(f"Phone input value: '{current_value}'")

        # Click Next button
        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button//div[contains(text(),'Next')]")
        ))
        next_button.click()

        # Wait for the verification code container to appear and extract code
        code_container = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[aria-details='link-device-phone-number-code-screen-instructions']")
        ))

        # Extract the code from the data-link-code attribute
        code = code_container.get_attribute("data-link-code")
        # Extract code by concatenating characters inside span elements
        chars = code_container.find_elements(By.CSS_SELECTOR, "span.x2b8uid")
        code_from_spans = "".join([c.text for c in chars])
        print("Verification code:", code_from_spans)
    finally:
        driver.quit()


def login_with_phone_number_alternative(phone_number):
    """Alternative approach using JavaScript execution"""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 180)

    try:
        driver.get("https://web.whatsapp.com/")

        # Click "Log in with phone number" button
        login_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(),'Log in with phone number')]")
        ))
        login_btn.click()

        # Input phone number field
        phone_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[aria-label='Type your phone number.']")
        ))

        # Use JavaScript to set the value directly
        full_number = f"+98{phone_number}"
        driver.execute_script("arguments[0].value = '';", phone_input)  # Clear with JS
        driver.execute_script("arguments[0].value = arguments[1];", phone_input, full_number)

        # Trigger input events to notify the page of the change
        driver.execute_script("""
            var element = arguments[0];
            var event = new Event('input', { bubbles: true });
            element.dispatchEvent(event);
        """, phone_input)

        # Verify the input value
        current_value = phone_input.get_attribute("value")
        # Click Next button
        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button//div[contains(text(),'Next')]")
        ))
        next_button.click()

        # Wait for the verification code container to appear and extract code
        code_container = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[aria-details='link-device-phone-number-code-screen-instructions']")
        ))

        # Extract the code from the data-link-code attribute
        code = code_container.get_attribute("data-link-code")
        # Extract code by concatenating characters inside span elements
        chars = code_container.find_elements(By.CSS_SELECTOR, "span.x2b8uid")
        code_from_spans = "".join([c.text for c in chars])
        print("Verification code :", code_from_spans)
    finally:
        driver.quit()


if __name__ == "__main__":
    phone = input("Enter your phone number without country code: ").strip()

    try:
        login_with_phone_number(phone)
    except Exception as e:
        login_with_phone_number_alternative(phone)