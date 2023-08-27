import os
import sys
import time
import openpyxl
from .person import Person
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Open the website and download the Excel file
def download_excel(driver, website, download_text, file_name, data_folder):
    driver.get(website)
    download_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//a[contains(text(), "{download_text}")]')
        )
    )
    f_name = f"./{data_folder}/{file_name}"
    if os.path.exists(f_name):
        os.remove(f_name)
    download_link.click()
    timeout = 10
    start_time = time.time()
    while not os.path.exists(f_name):
        if time.time() - start_time > timeout:
            print("Timeout: File download took too long. Bye...")
            sys.exit(1)
        time.sleep(0.5)
    prev_size = 0
    while os.path.getsize(f_name) > prev_size:
        prev_size = os.path.getsize(f_name)
    print("Download complete. Starting web interactions")


# Load the Excel workbook and process data
def process_excel_data(file_name, data_folder):
    f_name = f"./{data_folder}/{file_name}"
    workbook = openpyxl.load_workbook(f_name)
    sheet = workbook.active
    props = [str(cell.value).strip() for cell in sheet[1] if cell.value]
    persons_list = []
    for row_index, row in enumerate(sheet.iter_rows(), start=1):
        if row_index == 1:
            continue
        if row_index > 11:
            break
        row_data = [str(cell.value).strip() for cell in row if cell.value]
        persons_list.append(Person(props, row_data))
    return persons_list
