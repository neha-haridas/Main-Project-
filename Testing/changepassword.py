import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path=r"D:\PROJECT\MycardProjectect\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("http://127.0.0.1:8000/login/")
driver.maximize_window()


username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("neham2023b@mca.ajce.in")

password_field = driver.find_element(By.NAME, "pass")
password_field.send_keys("Varsha@123")
password_field.send_keys(Keys.RETURN)
time.sleep(5)

driver.get("http://127.0.0.1:8000/changepassword/")

oldpass_field = driver.find_element(By.NAME, "current_password")
oldpass_field.send_keys(str("Varsha@123"))

newpass_field = driver.find_element(By.NAME, "new_password")
newpass_field.send_keys(str("Varsha@1234"))


conpass_field = driver.find_element(By.NAME, "confirm_password")
conpass_field.send_keys(str("Varsha@1234"))
conpass_field.send_keys(Keys.RETURN)
time.sleep(5)

driver.get("http://127.0.0.1:8000/login/")
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("neham2023b@mca.ajce.in")

password_field = driver.find_element(By.NAME, "pass")
password_field.send_keys("Varsha@1234")
password_field.send_keys(Keys.RETURN)
time.sleep(5)

dashboard_element = driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome to')]")
if dashboard_element:
    print("Test Passed")
else:
    print("Test Failed")
time.sleep(3)
driver.quit()