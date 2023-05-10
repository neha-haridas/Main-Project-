import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path=r"D:\PROJECT\MycardProjectect\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()


driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("nehaharidas.m@gmail.com")

password_field = driver.find_element(By.NAME, "pass")
password_field.send_keys("Neha@123")
# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome to')]")
if dashboard_element:
    print("Login successful!")
else:
    print("Login failed.")

# Close the browser
driver.quit()