import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service('/usr/bin/geckodriver')
options = FirefoxOptions()

@pytest.fixture
def browser():
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_infinite_scroll(browser):
    browser.get("http://the-internet.herokuapp.com/infinite_scroll")
    
    paragraphs = browser.find_elements(By.CLASS_NAME, "jscroll-added")
    initial_count = len(paragraphs)
    
    for _ in range(5):
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)
        
    paragraphs = browser.find_elements(By.CLASS_NAME, "jscroll-added")
    new_count = len(paragraphs)
    
    assert new_count > initial_count, "No new content loaded after scrolling"
    
    browser.save_screenshot("infinite_scroll_result.png")
