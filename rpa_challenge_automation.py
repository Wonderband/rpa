import os
import sys
import time
from Modules import file_handling, web_forms, web_driver
from Modules.constants import (
    WEBSITE_URL,
    EXCEL_FILE_NAME,
    DATA_DIR,
    DOWNLOAD,
    START,
    SUBMIT,
)

# Create the DATA_DIR folder in the root directory and setup driver to download EXCEL_FILE_NAME file into this folder
try:
    file_handling.create_data_folder(DATA_DIR)
except Exception as e:
    print(f"Cannot create the folder for download: {e}")
    sys.exit(1)

path_to_file = f"./{DATA_DIR}/{EXCEL_FILE_NAME}"
driver = web_driver.setup(DATA_DIR)

# further manipulations with data and web forms
try:
    file_handling.download_excel(driver, WEBSITE_URL, DOWNLOAD, path_to_file)
except Exception as e:
    print(f"Error during download: {e}")
    sys.exit(1)

try:
    list_of_persons = file_handling.process_excel_data(path_to_file)
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
