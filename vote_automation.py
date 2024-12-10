import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import VOTING_URL, EMAIL_PREFIX, EMAIL_DOMAIN, INSTITUTION_NAME
from gmail_utility import fetch_otp

# Define the list of first names (non-formatted version)
first_names = [
    "aabha", "aadhya", "abha", "abhay", "abhinav", "adarsh", "aditya", "aishwarya", "akanksha", "alisha",
    "ananya", "anshika", "arjun", "asha", "ashwini", "avani", "ayesha", "bhavya", "bhoomika", "chirag",
    "chandana", "chitra", "divya", "gauri", "gita", "harika", "ishita", "jaya", "kajal", "karan",
    "kavya", "komal", "krishna", "lakshya", "manju", "madhuri", "mahi", "manisha", "maya", "meera",
    "mitali", "nandita", "nisha", "neha", "nikita", "omkar", "pooja", "pranavi", "pratik", "preeti",
    "radhika", "rajesh", "rekha", "rina", "rishi", "ritika", "rupali", "saanvi", "sakshi", "saloni",
    "sandeep", "shalini", "shivani", "simran", "sonal", "srishti", "siddharth", "tanya", "trisha",
    "tushar", "vandana", "varun", "vidhi", "vineeta", "vishal", "vivek", "yogesh", "yuvraj", "zara",
    "aarya", "abhav", "alina", "aarav", "anupriya", "archit", "amaya", "bhavika", "bipin", "bhavin",
    "chandan", "darsh", "dinesh", "deepak", "diya", "ekta", "falak", "gayatri", "ganesh", "hardik",
    "harsh", "hitesh", "iyer", "jagruti", "jayant", "jatin", "krish", "kushal", "lavanya", "leela",
    "madhavi", "manish", "mehak", "naitik", "navin", "neelam", "nitin", "pranav", "priyanka", "ravi",
    "rishabh", "rohit", "rupal", "shakshi", "shankar", "shanaya", "shubham", "siddhi", "suresh", "sumit",
    "tejas", "tulsi", "vatsal", "vidya", "vijay", "vinay", "vishnu", "yash", "yashika", "zain",
    "tanu", "suman", "sriya", "trilok", "tanish", "rudra", "samarth", "sarvesh", "shivendra", "shubhi",
    "sweta", "tanuja", "vaibhav", "vatsalya", "vibha", "sunil", "ruchi"
]


# Initialize the first name count
first_name_count = {name: 0 for name in first_names}
combined_names = []

# Generate random names, ensuring no first name is used more than twice
while len(combined_names) < len(first_names) * 2:  # Twice the number of first names
    first_name = random.choice(first_names)
    if first_name_count[first_name] < 2:  # Ensure no name is used more than twice
        combined_names.append(first_name)
        first_name_count[first_name] += 1

# Function to generate a random email
def random_email():
    """Generate a random email using the specified pattern."""
    return f"{EMAIL_PREFIX}{random.randint(1000, 9999)}{random.choice('abcdefghijklmnopqrstuvwxyz')}{EMAIL_DOMAIN}"

# Function to generate a random 10-digit phone number
def random_phone():
    """Generate a random 10-digit phone number."""
    return "".join([str(random.randint(0, 9)) for _ in range(10)])

# The main vote automation function
def vote():
    """Automate the voting process."""
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Make sure chromedriver is in PATH or the drivers folder

    try:
        while True:  # Infinite loop for continuous voting
            # Go to the voting URL
            driver.get(VOTING_URL)
            
            # Randomly select a full name
            full_name = random.choice(combined_names)

            # Click the "Vote For Us Here!" button
            vote_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/section/main[3]/section[1]/div/div[1]/div[2]/div/div[3]/a/button"))
            )
            vote_button.click()

            # Wait for the form popup
            time.sleep(2)  # Adjust as needed

            # Fill in the form fields
            driver.find_element(By.XPATH, "//*[@id='namehssl']").send_keys(full_name)  # Use first name
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
            time.sleep(10)

            # Handle OTP
            otp = fetch_otp()  # Assuming this function fetches OTP from your email
            otp_input = driver.find_element(By.XPATH, "//*[@id='otpUserHssl']")
            otp_input.send_keys(otp)

            # Click the "Submit" button
            submit_button = driver.find_element(By.XPATH, "//*[@id='hsslVotePopUp']/div[8]/div/button")
            submit_button.click()

            print(f"Vote successfully cast for {full_name}!")

            # Wait for 5 seconds before submitting the next vote
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    vote()
