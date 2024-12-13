from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

import os
import time
import random
from typing import Optional, List, Dict

class LinkedInAutomation:
    def __init__(self, headless: bool = False):
        """
        Initialize LinkedIn automation with configurable options

        Args:
            headless (bool, optional): Run the browser in headless mode. Defaults to False.
        """
        load_dotenv()

        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-infobars")      

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, email: Optional[str] = None, password: Optional[str] = None) -> bool:
        """
        Login to LinkedIn with provided credentials
        
        Args:
            email (str, optional): LinkedIn email address. Defaults to None.
            password (str, optional): LinkedIn password. Defaults to None.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        
        try:
            email = email or os.getenv('LINKEDIN_EMAIL')
            password = password or os.getenv('LINKEDIN_PASSWORD')

            if not email or not password:
                raise ValueError("LinkedIn credentials not provided.")
            
            self.driver.get("https://www.linkedin.com/login")

            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            email_field.send_keys(email)
            password_field.send_keys(password)

            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "nav[data-control-name='nav.navbar']"))
            )
            print("Login successful!")
            return True
        
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def go_to_network_page(self) -> None:
        self.driver.get("https://www.linkedin.com/mynetwork/")
        time.sleep(random.uniform(2, 4))

    def send_connection_requests(self, max_requests: int) -> int:
        """
        Send connection requests to users in the network page

        Args:
            max_requests (int, optional): Maximum number of connection requests to send.

        Returns:
            int: Number of connection requests sent.
        """
        self.go_to_network_page()
        requests_sent = 0
        try:
            while requests_sent < max_requests:
                connect_buttons = self.driver.find_elements(
                    By.XPATH, "//button[contains(@aria-label, 'Connect')]"
                )
                if not connect_buttons:
                    print("No more connection buttons found.")
                    break

                button = random.choice(connect_buttons)
                try:
                    button.click()
                    time.sleep(random.uniform(1.5, 3.5))
                    try:
                        send_button = self.driver.find_element(
                            By.XPATH, "//button[@aria-label='Send now']"
                        )
                        send_button.click()
                    except:
                        pass
                    sent_requests += 1
                    print(f"Sent request {sent_requests} / {max_requests}")
                    time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"Error sending connection requests: {e}")

        return sent_requests
    
    def close(self) -> None:
        if self.driver:
            self.driver.quit()

def main():
    bot = LinkedInAutomation(headless = True)
    try:
        if bot.login():
            request_sent = bot.send_connection_requests(max_requests = 20)
            print(f"Total Connection Requests Sent: {request_sent}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        bot.close()

if __name__ == "__main__":
    main()


            

