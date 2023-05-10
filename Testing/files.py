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
driver.get("http://127.0.0.1:8000/form/")
time.sleep(5)


# Find the file upload form and fill in the details
filename_input = driver.find_element(By.NAME,'filename')
filename_input.send_keys('my_file')
time.sleep(5)

descrip_input = driver.find_element(By.NAME,'descrip')
descrip_input.send_keys('my_file_description')
time.sleep(5)

pdf_input = driver.find_element(By.NAME,'pdf')
pdf_input.send_keys(r'D:\PROJECT\MycardProjectect\static\images\DATA_VISUALIZATION.pdf')
time.sleep(5)

# Submit the form
submit_button = driver.find_element('css selector', 'button[type="submit"]')
submit_button.click()

# Wait for the page to load and check for success message
time.sleep(3)  # Increase this if the page takes longer to load
print("File Upload  Successfull")

# Close the browser
driver.quit()