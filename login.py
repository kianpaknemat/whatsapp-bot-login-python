import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

BASE_SESSION_DIR = "session"


def setup_driver_with_session(phone_number):
    session_path = os.path.join(BASE_SESSION_DIR, phone_number)
    chrome_options = Options()

    if not os.path.exists(BASE_SESSION_DIR):
        os.makedirs(BASE_SESSION_DIR)

    if not os.path.exists(session_path):
        os.makedirs(session_path)

    chrome_options.add_argument(f"--user-data-dir={os.path.abspath(session_path)}")
    chrome_options.add_argument("--profile-directory=Default")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def check_existing_session(driver, wait_time=10):
    """Check if user is already logged in with existing session"""
    try:
        print("🔍 Checking for existing session...")
        driver.get("https://web.whatsapp.com/")
        wait = WebDriverWait(driver, wait_time)

        # Wait a bit for the page to load
        time.sleep(3)

        # Check multiple possible indicators that we're logged in
        try:
            # Method 1: Look for chat list
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")))
            print("✅ Session found! Already logged in to WhatsApp Web (chat-list detected).")
            return True
        except:
            pass

        try:
            # Method 2: Look for main app container
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app .two")))
            print("✅ Session found! Already logged in to WhatsApp Web (main app detected).")
            return True
        except:
            pass

        try:
            # Method 3: Check if we're NOT on login page (no QR code or login button)
            # If we don't see login elements, we might be logged in
            WebDriverWait(driver, 5).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Log in with phone number')]")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='qrcode']"))
                )
            )
            # If we reach here, login elements are present, so not logged in
            print("❌ No active session found. Login elements detected.")
            return False
        except:
            # If we can't find login elements, we might be logged in
            # Let's wait a bit more and check for any WhatsApp content
            time.sleep(5)

            # Check for any WhatsApp-specific elements that indicate we're logged in
            if driver.find_elements(By.CSS_SELECTOR, "[role='textbox']") or \
                    driver.find_elements(By.CSS_SELECTOR, ".lexical-rich-text-input") or \
                    driver.find_elements(By.CSS_SELECTOR, "[data-testid*='chat']"):
                print("✅ Session found! Already logged in to WhatsApp Web (content detected).")
                return True

            print("❌ No active session found. Need to login.")
            return False

    except Exception as e:
        print(f"❌ Session check failed: {str(e)}")
        return False


def confirm_session_saved(phone_number):
    session_path = os.path.join(BASE_SESSION_DIR, phone_number)
    if os.path.exists(session_path):
        print(f"📁 Session data has been stored in: {os.path.abspath(session_path)}")
    else:
        print("⚠️ Warning: Session folder not found after login.")


def login_with_phone_number(driver, phone_number):
    """Login using phone number when no session exists"""
    print("Starting phone number login process...")
    wait = WebDriverWait(driver, 180)

    try:
        # Click login with phone number button
        login_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(),'Log in with phone number')]")
        ))
        login_btn.click()

        # Enter phone number
        phone_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[aria-label='Type your phone number.']")
        ))

        phone_input.click()
        phone_input.clear()
        time.sleep(0.5)
        phone_input.send_keys(Keys.CONTROL + "a")
        phone_input.send_keys(Keys.DELETE)
        time.sleep(0.5)

        full_number = f"+98{phone_number}"
        phone_input.send_keys(full_number)
        time.sleep(1)

        # Click next button
        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button//div[contains(text(),'Next')]")
        ))
        next_button.click()

        # Get verification code
        code_container = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[aria-details='link-device-phone-number-code-screen-instructions']")
        ))

        chars = code_container.find_elements(By.CSS_SELECTOR, "span.x2b8uid")
        code_from_spans = "".join([c.text for c in chars])
        print("Verification code:", code_from_spans)
        input("After successfully logging into WhatsApp Web, press Enter to continue...")

        # Verify login success and save session
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")))
        print("✅ Login successful! Session has been saved.")
        confirm_session_saved(phone_number)
        return True

    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return False


def whatsapp_login(phone_number):
    """
    Main function to handle WhatsApp Web login with session management

    Args:
        phone_number (str): User's phone number for login

    Returns:
        webdriver: Chrome driver instance if successful, None if failed
    """
    print(f"🔄 Initializing WhatsApp Web login for: {phone_number}")

    # Step 1: Setup driver with session directory
    driver = setup_driver_with_session(phone_number)

    try:
        # Step 2: First check if user exists in session
        if check_existing_session(driver, wait_time=10):
            # Session found, user is already logged in
            return driver

        # Step 3: If user is not in session, use phone number for login
        print("🔐 No existing session found. Proceeding with phone number login...")

        # Make sure we're on WhatsApp Web page
        driver.get("https://web.whatsapp.com/")
        time.sleep(3)  # Give page time to load

        login_success = login_with_phone_number(driver, phone_number)

        if login_success:
            # Step 4: Session is automatically saved by Chrome when login succeeds
            print("💾 Session saved successfully!")
            return driver
        else:
            print("❌ Login process failed.")
            driver.quit()
            return None

    except Exception as e:
        print(f"❌ An error occurred during login: {str(e)}")
        driver.quit()
        return None


# Example usage function (for testing purposes)
def example_usage():
    phone_number = "9123456789"  # Replace with actual phone number
    driver = whatsapp_login(phone_number)

    if driver:
        print("🎉 WhatsApp Web is ready to use!")
        # Your WhatsApp automation code goes here
        # driver.quit()  # Uncomment when done
    else:
        print("💥 Failed to initialize WhatsApp Web")