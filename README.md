# Licenses Management Automation

This project automates license management by extracting data, synchronizing email lists, and revoking licenses using Selenium and CSV files.

## Project Structure

The project is organized as follows:

```plaintext
project/
│
├── main.py                  # Main script to run the workflow
│
├── src/                     # Source code organized into modules
│   ├── __init__.py          # Initializes the src package
│   ├── database.py          # Operations on PostgreSQL
│   ├── selenium_portal.py   # Functions for interacting with the license portal
│   └──  utils.py             # Utility functions (e.g., for CSV handling)
│
├── log/                     # Logs folder
│   └── script.log           # Log file generated by the application
│
├── data/                    # Folder for input and output CSV files
│   ├── input_email.csv      # Input email list from PostgreSQL
│   ├── exported_keys.csv    # Exported license keys from the portal
│   └──  revoked_keys.csv     # Log of revoked licenses
│
├── requirements.txt         # Dependencies required to run the project
└── README.md                # Documentation of the project
```


## Features

1. **Data Extraction from Database** 
   Extracts data from PostgreSQL and saves it to a CSV file.

2. **Selenium Automation**  
   - Logs into the license portal.
   - Downloads the list of assigned licenses.
   - Searches for specific emails and revokes corresponding licenses.

3. **CSV Management**  
   - Synchronizes two email lists and retains only common ones.
   - Saves results to organized CSV files.

## Prerequisites

- Python 3.8+
- Google Chrome and compatible ChromeDriver
- PostgreSQL (optional, for data extraction)
- Python modules specified in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project

2. Install dependencies:

    pip install -r requirements.txt

3. Configure the main variables in main.py and set file paths in the CSV files.

## Execution

Run the main script to execute the complete workflow:

python main.py

## Configuration

-   Logs: Log files are saved in the log/ folder.
-   Paths: Update the paths for CSV files or the driver in main.py or configuration files as needed.

## Contributions

Contributions are welcome! To propose changes, create a dedicated branch and submit a pull request.
