import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import VOTING_URL, EMAIL_PREFIX, EMAIL_DOMAIN, INSTITUTION_NAME
from gmail_utility import fetch_otp

def random_email():
    """Generate a random email using the specified pattern."""
    return f"{EMAIL_PREFIX}{random.randint(1000, 9999)}{random.choice('abcdefghijklmnopqrstuvwxyz')}{EMAIL_DOMAIN}"

def random_phone():
    """Generate a random 10-digit phone number."""
    return "".join([str(random.randint(0, 9)) for _ in range(10)])

def vote():
    """Automate the voting process."""
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Make sure chromedriver is in PATH or the drivers folder
    driver.get(VOTING_URL)

    try:
        # Click the "Vote For Us Here!" button
        vote_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/section/main[3]/section[1]/div/div[1]/div[2]/div/div[3]/a/button"))
        )
        vote_button.click()

        # Wait for the form popup
        time.sleep(2)  # Adjust as needed

        # Fill in the form fields
        driver.find_element(By.XPATH, "//*[@id='namehssl']").send_keys("John Doe")  # Replace with the voter's name
        driver.find_element(By.XPATH, "//*[@id='emailhssl']").send_keys(random_email())
        driver.find_element(By.XPATH, "//*[@id='contactNumberhssl']").send_keys(random_phone())

        # Select Grade from dropdown
        grade_dropdown = driver.find_element(By.XPATH, "//*[@id='gradeHssl']")
        grade_dropdown.click()
        driver.find_element(By.XPATH, "//*[@id='gradeHssl']/option[2]").click()

        # Enter Institution name
        driver.find_element(By.XPATH, "//*[@id='InstituteNamehssl']").send_keys(INSTITUTION_NAME)

        # Click the "Get OTP" button
        get_otp_button = driver.find_element(By.XPATH, "//*[@id='hsslVotePopUp']/div[5]/div/div/div/button")
        get_otp_button.click()

        # Wait for OTP to be sent (give it some time)
        time.sleep(5)

        # Handle OTP
        otp = fetch_otp()
        otp_input = driver.find_element(By.XPATH, "//*[@id='otpUserHssl']")
        otp_input.send_keys(otp)

        # Click the "Submit" button
        submit_button = driver.find_element(By.XPATH, "//*[@id='hsslVotePopUp']/div[8]/div/button")
        submit_button.click()

        print("Vote successfully cast!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    vote()
