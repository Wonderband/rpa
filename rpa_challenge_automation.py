import os
import sys
import time
from Modules import file_handling, web_forms, web_driver


# Constants for URLs, folders, filenames, and button texts on the target web page
WEBSITE_URL = "https://rpachallenge.com/"
EXCEL_FILE_NAME = "challenge.xlsx"
DATA_DIR = "dat"
DOWNLOAD = "Download Excel"
START = "Start"
SUBMIT = "Submit"

# Create the DATA_DIR folder in the root directory and setup driver to download EXCEL_FILE_NAME file into this folder
data_dir = os.path.join(os.path.dirname(__file__), DATA_DIR)
try:
    os.makedirs(data_dir, exist_ok=True)
except Exception as e:
    print(f"Cannot create the folder for download: {e}")
    sys.exit(1)

f_name = f"./{DATA_DIR}/{EXCEL_FILE_NAME}"
driver = web_driver.setup(DATA_DIR)

# further manipulations with data and web forms
try:
    file_handling.download_excel(driver, WEBSITE_URL, DOWNLOAD, f_name)
except Exception as e:
    print(f"Error during download: {e}")
    sys.exit(1)

try:
    list_of_persons = file_handling.process_excel_data(f_name)
except Exception as e:
    print(f"Error processing Excel data: {e}")
    sys.exit(1)

try:
    web_forms.start_challenge(driver, START)
    web_forms.fill_form_with_data(driver, list_of_persons, SUBMIT)
except Exception as e:
    print(f"Error during web interactions: {e}")
    sys.exit(1)
else:
    print("All done! Finishing...")

time.sleep(2)
driver.quit()
