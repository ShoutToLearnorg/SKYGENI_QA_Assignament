import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.base import get_driver, take_screenshot, remove_ads

def open_add_user_form(driver, wait):
    """
    Function to open the "Add User" form by clicking the add button.
    """
    add_button = wait.until(EC.element_to_be_clickable((By.ID, "addNewRecordButton")))
    add_button.click()

def fill_user_form(driver, wait, first_name, last_name, age, email, salary, department):
    """
    Function to fill out the user form with the provided data.
    """
    wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).send_keys(first_name)
    driver.find_element(By.ID, "lastName").send_keys(last_name)
    driver.find_element(By.ID, "age").send_keys(age)
    driver.find_element(By.ID, "userEmail").send_keys(email)
    driver.find_element(By.ID, "salary").send_keys(salary)
    driver.find_element(By.ID, "department").send_keys(department)

def get_age_input_border_color(driver):
    """
    Fetch the border color of the age input field. It handles the StaleElementReferenceException.
    """
    try:
        age_input = driver.find_element(By.ID, "age")
        return driver.execute_script(
            "return window.getComputedStyle(arguments[0]).borderColor;", age_input
        ).lower()
    except StaleElementReferenceException:
        # If the element becomes stale, re-find it and retry
        age_input = driver.find_element(By.ID, "age")
        return driver.execute_script(
            "return window.getComputedStyle(arguments[0]).borderColor;", age_input
        ).lower()

def test_add_user_invalid_age():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://demoqa.com/webtables")
        remove_ads(driver)
        
        # Open registration form
        add_button = wait.until(EC.element_to_be_clickable((By.ID, "addNewRecordButton")))
        add_button.click()
        
        # Fill form with invalid age
        age_input = wait.until(EC.visibility_of_element_located((By.ID, "age")))
        age_input.send_keys("ab")
        
        # Submit form
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        
        
        # Wait for border color change
        wait.until(
            lambda d: "rgb(220, 53, 69)" in d.execute_script(
                "return window.getComputedStyle(arguments[0]).borderColor;", 
                age_input
            ).lower()
        )

       
        
        # Verify form remains open
        assert submit_button.is_displayed()
        rows = driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group")
        assert not any("InvalidAge" in row.text for row in rows)
        
    finally:
         take_screenshot(driver, feature_folder="webtables", screenshot_name="test_add_user_invalid_age")
        
         driver.quit()

def test_delete_user():
    """
    Test to delete a user by email and ensure the deletion was successful.
    """
    driver = get_driver()
    wait = WebDriverWait(driver, 20)  # Increase timeout
    try:
        driver.get("https://demoqa.com/webtables")
        remove_ads(driver)

        target_email = "kierra@example.com"
        assert any(target_email in row.text for row in driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group"))

        delete_button = driver.find_element(
            By.XPATH, f"//div[text()='{target_email}']/ancestor::div[@class='rt-tr-group']//span[@title='Delete']"
        )
        delete_button.click()

        WebDriverWait(driver, 5).until_not(
            lambda d: any(target_email in row.text for row in d.find_elements(By.CSS_SELECTOR, "div.rt-tr-group"))
        )

        remaining_rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group") if r.is_displayed()]
        assert all(target_email not in row.text for row in remaining_rows)

    finally:
        take_screenshot(driver, feature_folder="webtables", screenshot_name="test_delete_user")
        driver.quit()

def test_search_user_by_email():
    """
    Test to search a user by email and verify that the correct user is displayed.
    """
    driver = get_driver()
    wait = WebDriverWait(driver, 20)  # Increase timeout
    try:
        driver.get("https://demoqa.com/webtables")
        remove_ads(driver)

        search_box = wait.until(EC.visibility_of_element_located((By.ID, "searchBox")))
        search_box.clear()
        search_box.send_keys("alden@example.com")

        wait.until(lambda d: any("alden@example.com" in row.text for row in d.find_elements(By.CSS_SELECTOR, "div.rt-tr-group")))

        visible_rows = [
            row for row in driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group")
            if row.is_displayed() and row.text.strip()
        ]

        assert len(visible_rows) == 1
        assert "alden@example.com" in visible_rows[0].text

    finally:
        take_screenshot(driver, feature_folder="webtables", screenshot_name="test_search_user_by_email")
        driver.quit()
