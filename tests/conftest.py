import pytest
import time
import os
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://localhost:5000"
TEST_USER = f"testuser_{int(time.time())}"
TEST_EMAIL = f"testuser_{int(time.time())}@test.com"
TEST_PASS = "testpass123"

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
SCREENSHOT_DIR = os.path.abspath(SCREENSHOT_DIR)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if driver:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            filename = f"{test_name}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            driver.save_screenshot(filepath)

            # Attach to Allure report ← ADD THIS
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )

            # Attach to HTML report
            if hasattr(report, "extra"):
                from pytest_html import extras
                report.extra = getattr(report, "extra", [])
                report.extra.append(extras.image(filepath))

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def logged_in_driver(driver):
    """Returns a driver that is already logged in."""
    # Clear any existing session
    driver.delete_all_cookies()

    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.ID, "identifier")))
    driver.find_element(By.ID, "identifier").send_keys(TEST_USER)
    driver.find_element(By.ID, "password").send_keys(TEST_PASS)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-submit")))
    driver.find_element(By.CSS_SELECTOR, "button.btn-submit").click()

    # Wait until redirected away from login page
    wait.until(EC.url_to_be(f"{BASE_URL}/"))

    return driver
