import os
import logging
import pandas as pd 

def join_downloaded_with_input(input_email_path, download_dir, exported_keys):
    """Load 'input_email.csv' and 'My Keys.csv', perform an inner join on specified columns."""
    try:
        # Load input email CSV
        input_df = pd.read_csv(input_email_path)
        print("Input data from Postgres:")
        print(input_df)
        
        # Load the downloaded keys CSV
        downloaded_keys_path = os.path.join(download_dir, exported_keys)
        keys_df = pd.read_csv(downloaded_keys_path)
        keys_df['Assigned Email'] = keys_df['Assigned Email'].str.lower()
        
        # Filter the emails from input_email.csv that are present in My Keys.csv
        # Assume 'Assigned Email' is the column containing the email in My Keys.csv
        # And 'Email ID' is the column with emails in input_email.csv
        common_emails = input_df[input_df['Email ID'].isin(keys_df['Assigned Email'])]
        logging.info("Filtered emails df created")
        
        return common_emails  # Returns the filtered DataFrame
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        logging.error(f"Empty data error: {e}")
    except Exception as e:
        logging.error(f"An error occurred during the join operation: {e}")