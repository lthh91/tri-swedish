"""
Needed utilities
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def get_driver(headless=True):
    """
    Returns a selenium driver
    """
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)
    return driver


def generate_cookie(driver, url):
    """
    Returns cookies of a website
    """
    driver.get(url)
    cookies = driver.get_cookies()
    converted_cookies = {item['name']: item['value'] for item in cookies}
    return converted_cookies
