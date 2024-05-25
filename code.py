from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import os
import time
import requests


# URL of the login page
url = 'https://ht.juwa777.com/login'  # Replace with the actual URL of your login page

# Path to the ChromeDriver
chromedriver_path = 'C:\Program Files\chromedriver-win64\chromedriver-win64/chromedriver.exe'  # Replace with the actual path to your ChromeDriver

# Folder to save CAPTCHA images
os.makedirs('captchas', exist_ok=True)

# Function to fetch and save CAPTCHA images
def fetch_captcha_images(url, count=500):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Setup Chrome WebDriver
    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    for i in range(count):
        # Navigate to the login page
        driver.get(url)

        try:
            # Wait until the CAPTCHA image is present
            img_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img.imgCode'))
            )
            
            # Get the CAPTCHA image URL
            img_url = img_tag.get_attribute('src')
            print(f"Found CAPTCHA image URL: {img_url}")

            # Fetch the CAPTCHA image
            img_response = requests.get(img_url)
            img = Image.open(BytesIO(img_response.content))

            # Save the CAPTCHA image
            img.save(f'captchas/captcha_{i+1}.png')
            print(f'Saved captcha_{i+1}.png')

            # Wait a bit to avoid overloading the server
            time.sleep(1)

        except Exception as e:
            print(f"Error fetching CAPTCHA image: {e}")

    # Quit the WebDriver
    driver.quit()

# Fetch and save 70 CAPTCHA images
fetch_captcha_images(url)
