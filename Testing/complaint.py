import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


service = Service(executable_path=r"D:\PROJECT\MycardProjectect\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()


driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("neham2023b@mca.ajce.in")

password_field = driver.find_element(By.NAME, "pass")
password_field.send_keys("Varsha@1234")

# Submit the login form
password_field.send_keys(Keys.RETURN)
time.sleep(5)

# Navigate to the complaint page
driver.get("http://127.0.0.1:8000/StudentBookScomplaint/")
time.sleep(5)

# Enter a complaint message
complaint_input = driver.find_element(By.NAME,"complaint_msg")
complaint_input.send_keys("This is a test complaint.")
time.sleep(5)

# Submit the complaint form
submit_button = driver.find_element('css selector',"input[type='submit']")
submit_button.click()

# Wait for the page to load
time.sleep(5)
print("Complaint Sent  Successfull")

# Close the browser window
driver.quit()
