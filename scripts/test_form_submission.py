import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # <-- ADD THIS LINE
from utils.base import get_driver, take_screenshot

def test_valid_form_submission():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://demoqa.com/automation-practice-form")
        
        # Fill form with explicit waits
        wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).send_keys("Ashish")
        driver.find_element(By.ID, "lastName").send_keys("Kumar")
        driver.find_element(By.ID, "userEmail").send_keys("ashish@gmail.com")
        
        # Gender selection with scroll and JS click
        gender_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Male']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", gender_label)
        driver.execute_script("arguments[0].click();", gender_label)
        
        driver.find_element(By.ID, "userNumber").send_keys("1234567890")
        
        # Submit with JS click
        submit_button = wait.until(EC.presence_of_element_located((By.ID, "submit")))
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Verification
        confirmation = wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
        assert "Thanks for submitting the form" in confirmation.text
        take_screenshot(driver, "form", "valid_submission")
        
    except Exception as e:
        take_screenshot(driver, "form", "valid_submission_fail")
        raise e
    finally:
        driver.quit()

def test_missing_gender_validation():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://demoqa.com/automation-practice-form")
        
        # Submit form without gender
        submit_button = wait.until(EC.presence_of_element_located((By.ID, "submit")))
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Verify 1: Form submission blocked (no success modal)
        with pytest.raises(TimeoutException):
            wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
            
        # Verify 2: Label text turns red
        gender_label = driver.find_element(By.XPATH, "//label[@for='gender-radio-1']")
        label_color = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).color;", 
            gender_label
        )
        assert "220, 53, 69" in label_color  # Verify red text color
        
        take_screenshot(driver, "form", "missing_gender_error")
        
    except Exception as e:
        take_screenshot(driver, "form", "missing_gender_fail")
        raise e
    finally:
        driver.quit()



def check_invalid_field(driver, element):
    """Verify field shows invalid state using CSS pseudo-classes"""
    # Check browser validation state
    is_invalid = driver.execute_script(
        "return arguments[0].matches(':invalid') && !arguments[0].validity.valid;", 
        element
    )
    assert is_invalid, "Field should show invalid state"
    
    # Verify visual styling
    border_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).borderColor;",
        element
    )
    assert "220, 53, 69" in border_color  # RGB for #dc3545

def check_invalid_field(driver, element):
    """Verify field shows invalid state using CSS pseudo-classes"""
    # Check browser validation state
    is_invalid = driver.execute_script(
        "return arguments[0].matches(':invalid') && !arguments[0].validity.valid;", 
        element
    )
    assert is_invalid, "Field should show invalid state"
    
    # Verify visual styling
    border_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).borderColor;",
        element
    ).lower().replace(" ", "").replace("(", "").replace(")", "")
    
    # Normalize expected value and actual value
    assert "220,53,69" in border_color, f"Border color {border_color} doesn't contain validation red"



@pytest.mark.xfail(reason="Known issue: Calendar allows future dates")
def test_future_date_of_birth():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://demoqa.com/automation-practice-form")
        
        # Open date picker
        date_input = wait.until(EC.element_to_be_clickable((By.ID, "dateOfBirthInput")))
        date_input.click()
        
        # Try to select future date
        future_date = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".react-datepicker__day--outside-month")
        ))
        future_date.click()
        
        # Verify date was not accepted (update year as needed)
        selected_date = date_input.get_attribute("value")
        assert "2024" not in selected_date  # Update year based on current date
        
    except Exception as e:
        take_screenshot(driver, "form", "future_date_fail")
        raise e
    finally:
        driver.quit()

def test_future_date_of_birth():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://demoqa.com/automation-practice-form")
        
        # Open date picker
        date_input = wait.until(EC.element_to_be_clickable((By.ID, "dateOfBirthInput")))
        date_input.click()
        
        # Try to select future date (implementation specific)
        # This will fail because the calendar allows future dates (as per user note)
        future_date = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".react-datepicker__day--outside-month")
        ))
        future_date.click()
        
        # Verify date was not accepted
        selected_date = date_input.get_attribute("value")
        assert "2024" not in selected_date  # This assertion will fail intentionally
        
    except Exception as e:
        take_screenshot(driver, "form", "future_date_fail")
        raise e
    finally:
        driver.quit()