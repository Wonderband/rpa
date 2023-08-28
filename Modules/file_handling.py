import os
import sys
import time
import openpyxl
from .person import Person
from .constants import NUMBER_OF_RECORDS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Create folder for storing file with data
def create_data_folder(folder_name):
    parent_directory_path = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(parent_directory_path, folder_name)
    os.makedirs(data_dir, exist_ok=True)


# Open the website and download the Excel file
def download_excel(driver, website, download_text, file_name):
    driver.get(website)
    download_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//a[contains(text(), "{download_text}")]')
        )
    )
    if os.path.exists(file_name):
        os.remove(file_name)
    download_link.click()
    timeout = 10
    start_time = time.time()
    while not os.path.exists(file_name):
        if time.time() - start_time > timeout:
            print("Timeout: File download took too long. Bye...")
            sys.exit(1)
        time.sleep(0.5)
    prev_size = 0
    while os.path.getsize(file_name) > prev_size:
        time.sleep(0.5)
        prev_size = os.path.getsize(file_name)
    print("Download complete. Starting web interactions")


# Load the Excel workbook and process data
def process_excel_data(file_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    persons_list = []
    for row_index, row in enumerate(sheet.iter_rows(), start=1):
        if row_index > NUMBER_OF_RECORDS + 1:
            break
        row_data = [str(cell.value).strip() for cell in row if cell.value]
        if row_index == 1:
            props = row_data
            continue
        persons_list.append(Person(props, row_data))
    return persons_list
