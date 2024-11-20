import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv

def setup_driver(driver_path, link):
    os.environ['PATH'] += os.pathsep + os.path.dirname(driver_path)
    try:
        """Initialize the Chrome driver with specific download settings."""
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(link)
        logging.info("Driver returned.")
        return driver
    except:
        logging.error("Error in driver returning")

def accept_cookies(driver):
    """Accept cookies if the prompt is available."""
    try:
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies_button.click()
        logging.info("Clicked 'Accept All Cookies' button.")
    except NoSuchElementException:
        logging.warning("'Accept All Cookies' button not found.")

def login(driver, username, password):
    """Log in to the Tableau Customer Portal."""
    try:
        # Input username and password
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[2]/form[1]/div[1]/input[1]'))
        )
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'login_password'))
        )
        password_field.send_keys(password)

        # Click the login button
        login_button = driver.find_element(By.ID, "signInButton")
        driver.execute_script("arguments[0].click();", login_button)
        WebDriverWait(driver, 20).until(EC.url_contains("my-keys"))
        logging.info("Login completed successfully.")
    except TimeoutException:
        logging.error("Timeout during login.")
        driver.quit()

def download_exported_data(driver, download_folder):
    """Clicks the 'Export Data' button and the 'CSV' button, then waits for the download to complete."""
    try:
        # Wait until the page is fully loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.dt-button.buttons-collection"))
        )
        
        # Check that the 'Export Data' button is clickable
        export_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.dt-button.buttons-collection"))
        )
        
        # Click the button to start the download
        export_button.click()
        logging.info("Clicked the 'Export Data' button to start download.")
        
        # Wait until the 'CSV' button is visible and clickable
        csv_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.dt-button.buttons-csv.buttons-html5.buttons-export"))
        )
        
        # Click the 'CSV' button
        csv_button.click()
        logging.info("Clicked the 'CSV' button to export the data as CSV.")
        
        # Wait for download completion
        download_complete = False
        while not download_complete:
            time.sleep(1)  # Short pause between checks
            download_complete = any(
                file.endswith(".csv") and not file.endswith(".crdownload") 
                for file in os.listdir(download_folder)
            )
        logging.info("Download complete, file ready for processing.")
        
    except TimeoutException:
        logging.error("Export Data button or CSV button not found or not clickable.")

def search_for_email(driver, link, email):
    """Search for the email in the customer asset search bar."""
    try:
        # Reload the page for each new email
        driver.get(link)
        WebDriverWait(driver, 20).until(EC.url_contains("my-keys"))
        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tbl_Customer_Asset__c_filter"))
        )
        search_bar = driver.find_element(
                By.XPATH, '/html[1]/body[1]/div[3]/div[2]/div[1]/div[3]/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[5]/div[3]/div[1]/div[1]/div[2]/label[1]/input[1]'
        )
        search_bar.clear()
        search_bar.send_keys(email)
        logging.info(f"Searching for email: {email}")
        time.sleep(3)
        return True
    except TimeoutException:
        logging.warning(f"Timeout during search for email: {email}")
        return False

def extract_license_key(driver,link, email):
    """Extracts the license key for a specific email."""
    try:
        # Search for the email in the Customer Portal
        if search_for_email(driver, link, email):
            logging.info(f"Found {email}, extracting license key...")
            # Click the Key Name to access license details
            key_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Key_Name'))
            )
            key_element.click()
            logging.info("Key name clicked.")
            time.sleep(5)  # Wait for the details to load
        
        # Waits for and retrieves the license key text element
        license_key_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.uiOutputTextArea"))
        )
        license_key = license_key_element.text
        logging.info(f"License key extracted: {license_key}")
        return license_key
    except TimeoutException:
        logging.error("Unable to retrieve the license key.")
        return None

def unassign_key(driver, email, license_key, output_keys):
    """Unassigns the license and logs the result in the CSV."""
    try:
        # Finds and clicks the 'Unassign Key' button
        unassign_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn-unassign-key"))
        )
        unassign_button.click()
        logging.info("'Unassign Key' button clicked.")
        time.sleep(2)  # Waits for the unassignment operation to complete
        
        # Writes to the CSV only if unassignment is successful
        with open(output_keys, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, license_key])
            logging.info(f"License unassigned and logged in CSV for email: {email}")
    except TimeoutException:
        # Logs the email as failed in case of error
        with open(output_keys, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, "Unassignment failed"])
        logging.warning(f"Unassignment failed for email: {email}")
