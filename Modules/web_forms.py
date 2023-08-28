from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Click the "Start" button to begin data entry
def start_challenge(driver, start_text):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//button[text()="{start_text}"]'))
    )
    button.click()


# Fill in data for each person and submit
def fill_form_with_data(driver, persons_list, submit_value):
    for person in persons_list:
        for key, value in vars(person).items():
            label_element = driver.find_element(By.XPATH, f'//label[text()="{key}"]')
            input_element = label_element.find_element(
                By.XPATH, "./following-sibling::input"
            )
            input_element.clear()
            input_element.send_keys(value)
        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//input[@type="submit" and @value="{submit_value}"]')
            )
        )
        submit.click()
