import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


# Attempt to detect the installed browser and set up the appropriate WebDriver
def is_chrome_installed():
    return "chrome" in webdriver.__dict__


def is_firefox_installed():
    return "firefox" in webdriver.__dict__


# Set up Chrome WebDriver with custom download options
def setup_chrome_driver(data_folder):
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": data_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    return webdriver.Chrome(options=chrome_options)


# Set up Firefox WebDriver with custom download options
def setup_firefox_driver(data_folder):
    firefox_options = FirefoxOptions()
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.dir", data_folder)
    firefox_options.set_preference("browser.download.useDownloadDir", True)
    firefox_options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    return webdriver.Firefox(options=firefox_options)


def setup(folder):
    parent_directory_path = os.path.dirname(os.path.dirname(__file__))
    data_folder = parent_directory_path + f"\{folder}"
    if is_chrome_installed():
        print("We'll work on Chrome!")
        return setup_chrome_driver(data_folder)

    elif is_firefox_installed():
        print("We'll work on Firefox!")
        return setup_firefox_driver(data_folder)
    else:
        print("No compatible browser found. Bye...")
        sys.exit(1)
