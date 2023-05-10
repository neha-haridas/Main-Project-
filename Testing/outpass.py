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
password_field.send_keys("Varsha@123")

# Submit the login form
password_field.send_keys(Keys.RETURN)
time.sleep(5)

# Navigate to the complaint page
driver.get("http://127.0.0.1:8000/Outpass/")

name_field = driver.find_element(By.NAME,'name')
name_field.send_keys('Varsha J J ')

dept_field = driver.find_element(By.NAME,'dept')
dept_field.send_keys('Computer Science')

sem_field = driver.find_element(By.NAME,'sem')
sem_field.send_keys('3rd')

mobno_field = driver.find_element(By.NAME,'mobno')
mobno_field.send_keys('8567493210')

ldate_field = driver.find_element(By.NAME,'ldate')
ldate_field.send_keys('10-05-2023 10:31')

idate_field = driver.find_element(By.NAME,'idate')
idate_field.send_keys('15-05-2023 10:31')

purpose_field = driver.find_element(By.NAME,'purpose')
purpose_field.send_keys('Going home for family emergency')

dest_field = driver.find_element(By.NAME,'dest')
dest_field.send_keys('Wayanad')

parents_email_field = driver.find_element(By.NAME,'parents_email')
parents_email_field.send_keys('nehaharidas.m@gmail.com')
time.sleep(5)

parents_contact_field = driver.find_element(By.NAME,'parents_contact')
parents_contact_field.send_keys('9876543210')
time.sleep(5)

submit_button = driver.find_element('css selector',"input[type='submit']")
submit_button.click()
time.sleep(5)

# Wait for the confirmation page to load
confirmation_message = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//h3[text()='Outpass History']"))
)


# Close the webdriver
driver.quit()