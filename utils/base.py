# utils/base.py (Fixed and Optimized)
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

def get_driver(headless=False):
    """Create and configure a Chrome WebDriver instance"""
    chrome_options = Options()
    
    # Essential stability arguments
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Window management
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        chrome_options.add_argument("--start-maximized")

    # Configure driver service
    service = Service(ChromeDriverManager().install())
    
    # Create driver instance
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Block ad networks
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": [
            "*.doubleclick.net",
            "*.googleadservices.com",
            "*.adservice.google.com",
            "*.adsrvr.org"
        ]
    })
    driver.execute_cdp_cmd("Network.enable", {})
    
    return driver

def remove_ads(driver):
    """Remove common ad elements from the DOM"""
    driver.execute_script("""
    const ads = document.querySelectorAll(
        'div[class*="ad"], iframe[src*="ad"], div.popup, div.overlay'
    );
    ads.forEach(ad => ad.remove());
    """)
    return driver

def take_screenshot(driver, feature_folder, screenshot_name, element=None):
    """
    Capture and save a screenshot
    :param driver: WebDriver instance
    :param feature_folder: Category for organizing screenshots
    :param screenshot_name: Base name for the screenshot file
    :param element: Optional element to scroll into view
    :return: Path to saved screenshot
    """
    try:
        # Create directory structure
        screenshot_dir = os.path.join("screenshots", feature_folder)
        os.makedirs(screenshot_dir, exist_ok=True)

        # Prepare view
        driver.maximize_window()
        remove_ads(driver)

        # Scroll to element if specified
        if element:
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                element
            )
            time.sleep(0.5)  # Allow smooth scroll completion

        # Wait for UI stability
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading, .spinner"))
        )
        
        # Generate filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(
            screenshot_dir, 
            f"{screenshot_name}_{timestamp}.png"
        )
        
        # Capture screenshot
        driver.save_screenshot(filename)
        return filename

    except Exception as e:
        # Emergency fallback
        error_dir = os.path.join("screenshots", "errors")
        os.makedirs(error_dir, exist_ok=True)
        emergency_path = os.path.join(error_dir, f"emergency_{int(time.time())}.png")
        driver.save_screenshot(emergency_path)
        print(f"Screenshot error: {str(e)}")
        return emergency_path