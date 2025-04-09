import datetime
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import tkinter as tk
from tkinter import messagebox
from selenium.webdriver.chrome.service import Service
# ======= CONFIGURATION =======
URL = "https://anny.co/b/en-us/book/volleyball-ii?step=calendar&s=ybpxjllvk3zl67ykdx4jpgjiiefa3x"
#TODO: Es Reicht einfach nur https://anny.co/b/en-us/book/volleyball-ii den rest kannst du wie bei mir dann unten im driver direkt machen
# Registration details:
FIRST_NAME = "Mouad1"
LAST_NAME = "Meziani2"
EMAIL = "se.mouadmeziani@gmail.com"

# ----- Notification Options -----
USE_POPUP = True   # Set to False if you prefer only console messages.

# ----- Brave Browser Setup -----
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# ----- ChromeDriver Setup -----
CHROMEDRIVER_PATH = r"D:\programms\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def notify_user(message):
    print(message)
    if USE_POPUP:
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Registration Notification", message)
        except Exception as e:
            print("Popup failed:", e)

def get_next_thursday():
    """
    Compute the date for the next Thursday.
    """
    # Geht das nicht irgendwie einfacher? scheint mit so kompliziert haha, würde ich an deiner stelle eher über einen cronjob lösen 
    today = datetime.date.today()
    # Thursday is weekday 3 (Monday is 0)
    days_ahead = (3 - today.weekday() + 7) % 7
    if days_ahead == 0:
        days_ahead = 7
    return today + datetime.timedelta(days=days_ahead)

def select_thursday_date(driver, wait):
    target_date = get_next_thursday()
    target_day = str(target_date.day)
    # Build XPath to select a div with class "date-item" whose title contains "Donnerstag"
    # and which contains a child div with the day number.
    xpath = (
        f"//div[contains(@class, 'date-item') and contains(@title, 'Donnerstag') "
        f"and .//div[normalize-space(text())='{target_day}']]"
    )
    
    try:
        date_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        notify_user(f"Could not find a clickable element for Thursday ({target_day}).")
        return False
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", date_element)
        try:
            date_element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", date_element)
    except Exception as e:
        notify_user("Error clicking on the Thursday date: " + str(e))
        return False
    return True
    #TODO: Du Brauchst das hier nicht, du kannst einfach auf Continue klicken, der Tag ist direkt autoamtisch ausgewählt gibt ja nur einen

def register_volleyball():
    success = False
    print(f"Starting registration process at {datetime.datetime.now()}")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Remove this argument to watch the browser.
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu") # Hab ich mal hinzugefüht hat mir chatgpt angegeben 
        options.binary_location = BRAVE_PATH

        
        service = Service(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 20)
        driver.get(URL)
        #TODO: würde es halt über cronjob lösen 
        # Select next Thursday's date (only selectable day)
        if not select_thursday_date(driver, wait):
            driver.quit()
            return False

        # Click the "Continue" button with a JS fallback
        try:
            continue_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Continue')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
            try:
                continue_btn.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", continue_btn)
        except TimeoutException:
            notify_user("Could not find the 'Continue' button.")
            driver.quit()
            return False

        # Check if there are available times
        try:
            no_times = driver.find_elements(By.XPATH, "//*[contains(text(), 'There are no times to choose from')]")
            if no_times:
                notify_user("Registration failed: No available time slots for the selected Thursday.")
                driver.quit()
                return False
        except Exception:
            pass

        # Fill out the registration form
        try:
            first_name_field = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
            last_name_field = driver.find_element(By.NAME, "lastName")
            email_field = driver.find_element(By.NAME, "email")

            first_name_field.clear()
            first_name_field.send_keys(FIRST_NAME)

            last_name_field.clear()
            last_name_field.send_keys(LAST_NAME)

            email_field.clear()
            email_field.send_keys(EMAIL)
        except TimeoutException:
            notify_user("Registration form did not load in time.")
            driver.quit()
            return False
        except NoSuchElementException:
            notify_user("Could not locate registration form fields.")
            driver.quit()
            return False

        try:
            agree_checkbox = driver.find_element(By.ID, "agree")
            if not agree_checkbox.is_selected():
                agree_checkbox.click()
        except NoSuchElementException:
            pass

        # Submit the form
        try:
            #TODO: Funktioniert das? 
            submit_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Register') or contains(., 'Submit')]")))
            #TODO: Wenn du das headless machst, kannst du das fenster auf ne größe machen dann siehst der alles und muss nicht scrollen 
            # irgendwie so options.add_argument("window-size=1920,2000")
            # Das mit dem scrollen hat nicht ganz funktioniert bei mir darum haha
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            try:
                submit_btn.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", submit_btn)
        except TimeoutException:
            notify_user("Could not click the submit button.")
            driver.quit()
            return False

        # Check for confirmation message
        try:
            #TODO: Das smart muss ich mal gucken ob ich das dir das klaue
            confirmation = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Thank you') or contains(text(), 'confirmed')]")))
            notify_user("Registration successful!")
            success = True
        except TimeoutException:
            notify_user("No confirmation received; registration might not have been successful.")
            success = False

        driver.quit()
    except Exception as e:
        print("An error occurred during registration:")
        traceback.print_exc()
        notify_user("An error occurred during registration. Check logs for details.")
        success = False

    return success

if __name__ == "__main__":
    register_volleyball()
