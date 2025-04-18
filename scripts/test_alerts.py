import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.base import get_driver, take_screenshot

def test_simple_alert():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://demoqa.com/alerts")
        
        # Handle ads and wait for button to be clickable
        button = wait.until(EC.element_to_be_clickable((By.ID, "alertButton")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)
        
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        take_screenshot(driver, "alerts", "simple_alert_accepted")
    except Exception as e:
        take_screenshot(driver, "alerts", "simple_alert_fail")
        raise e
    finally:
        driver.quit()

def test_confirm_alert_dismiss():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://demoqa.com/alerts")
        
        # Use JavaScript click to bypass overlays
        button = wait.until(EC.presence_of_element_located((By.ID, "confirmButton")))
        driver.execute_script("arguments[0].click();", button)
        
        alert = wait.until(EC.alert_is_present())
        alert.dismiss()
        result = driver.find_element(By.ID, "confirmResult")
        assert "Cancel" in result.text
        take_screenshot(driver, "alerts", "confirm_dismissed")
    except Exception as e:
        take_screenshot(driver, "alerts", "confirm_dismiss_fail")
        raise e
    finally:
        driver.quit()