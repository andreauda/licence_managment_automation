from src import *
import time
import logging
import details as det
import datetime as datetime

# Configure logging to save logs to a file
today_date = datetime.datetime.now().strftime(f'%Y-%m-%d')
log_filename = f'log/log_{today_date}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Keeps the output on the console
    ]
)

# Scrip Starting
logging.info("""
             SCRIPT STARTED
             """)

### Calling Variables from details.py ###

# Postgres details
host = det.host
db = det.database
db_user = det.db_user
db_pass = det.db_pass
# Customer Portal details
link = det.link  
username = det.cp_user
cp_pass = det.cp_pass
# ChromeDriver Path
driver_path = det.driver_path
# filename with data extracted from Postgres                  
data_from_postgres = det.input_email  
# filename and path of data extracted from Customer Portal  
exported_keys = det.exported_keys
download_dir = det.download_dir         # path
# final file with emails and keys
output_keys = det.output_keys

### main() ###

def main():
    """Main function to execute the workflow."""
    driver = setup_driver(driver_path, link)
    time.sleep(1)
    accept_cookies(driver)
    time.sleep(2)
    login(driver, username, cp_pass)
    time.sleep(5)
    
    # Download all data
    download_exported_data(driver, download_dir)
    
    # Load and filter CSVs based on common emails
    common_emails_df = join_downloaded_with_input(data_from_postgres, download_dir, exported_keys)  # Capture filtered DataFrame
    common_emails_df.drop_duplicates()
    print("Common Emails: ")
    print(common_emails_df)
    
    # Check if the merged DataFrame is empty
    if common_emails_df.empty:
        logging.warning("No data to process after merging.")
        driver.quit()
        return
    
    # Process each email in the merged DataFrame
    for index, row in common_emails_df.iterrows():
        driver.refresh()
        # Then in the main:
        email = row['Email ID']
        license_key = extract_license_key(driver,link, email)
        if license_key:
            time.sleep(5)
            unassign_key(driver, email, license_key, output_keys)
        else:
            logging.error(f"No license key found for email: {email}")
    
    driver.quit()  # Ensures driver closes at the end
    logging.info("Process completed.")

if __name__ == "__main__":
    main()