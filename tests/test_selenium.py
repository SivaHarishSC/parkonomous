import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
class ParkonomousTest(unittest.TestCase):
    """
    Test case for Parkonomous application.
    """

    def setUp(self):
        """
        Set up the Chrome WebDriver and navigate to the app URL.
        """
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")  # Ensure the app is running on this address

    def tearDown(self):
        """
        Clean up after each test by quitting the WebDriver.
        """
        self.driver.quit()

    def test_registration_and_login(self):
        """
        Test the registration and login functionality.
        """
        driver = self.driver

        # Registration
        print("=== Registration ===")
        driver.find_element(By.LINK_TEXT, "Register").click()
        WebDriverWait(driver, 10).until(EC.title_contains("Registration"))
        print("Clicked on Register link and on Registration page")

        driver.find_element(By.NAME, "name").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "contact").send_keys("1234567890")
        driver.find_element(By.NAME, "vehicle_id").send_keys("98765")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Ensure registration is successful
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success")))
        print("Registration successful")

        # Login
        print("=== Login ===")
        driver.find_element(By.NAME, "name").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Check if login is successful by confirming the title of the home page
        try:
            WebDriverWait(driver, 10).until(EC.title_contains("Parkonomous"))
            print("Login successful, landed on Parkonomous home page")
        except TimeoutException as e:
            # Print out the current page title and URL for debugging
            print(f"Current title: {driver.title}")
            print(f"Current URL: {driver.current_url}")
            raise e

        # Confirm the user is redirected to the home page
        self.assertIn("Parkonomous", driver.title)

        # Navigate to About Us page
        print("=== Navigate to About Us ===")
        self.navigate_to_about_us()

        # Navigate to Map (Service) page
        print("=== Navigate to Map (Service) ===")
        self.navigate_to_map_page()

        # Navigate back to Home page
        print("=== Navigate to Home page ===")
        self.navigate_to_home_page()

    def navigate_to_about_us(self):
        """
        Navigate to the About Us page.
        """
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "About Us"))).click()
            WebDriverWait(driver, 10).until(EC.title_contains("About Us"))
            print("Navigated to About Us page successfully")
        except TimeoutException as e:
            # Print out the current page title and URL for debugging
            print(f"About Us page - Current title: {driver.title}")
            print(f"About Us page - Current URL: {driver.current_url}")
            print(driver.page_source)  # Print page source to help debug
            raise e

        # Confirm navigation to About Us page
        self.assertIn("About Us", driver.title)

    def navigate_to_map_page(self):
        """
        Navigate to the Map (Service) page.
        """
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Map"))).click()
            WebDriverWait(driver, 10).until(EC.title_contains("Map"))
            print("Navigated to Map page successfully")
        except TimeoutException as e:
            # Print out the current page title and URL for debugging
            print(f"Map page - Current title: {driver.title}")
            print(f"Map page - Current URL: {driver.current_url}")
            print(driver.page_source)  # Print page source to help debug
            raise e

        # Confirm navigation to Map page
        self.assertIn("Map", driver.title)

    def navigate_to_home_page(self):
        """
        Navigate to the Home page.
        """
        driver = self.driver
        try:
            driver.get("http://localhost:5000/home")
            WebDriverWait(driver, 10).until(EC.title_contains("Parkonomous"))
            print("Navigated to Home page successfully")
        except TimeoutException as e:
            # Print out the current page title and URL for debugging
            print(f"Home page - Current title: {driver.title}")
            print(f"Home page - Current URL: {driver.current_url}")
            print(driver.page_source)  # Print page source to help debug
            raise e

        # Confirm navigation to Home page
        self.assertIn("Parkonomous", driver.title)

if __name__ == "__main__":
    unittest.main()
