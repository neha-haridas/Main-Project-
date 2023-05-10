
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


service = Service(executable_path=r"D:\PROJECT\MycardProjectect\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()


driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("llibrarianmycard@gmail.com")

password_field = driver.find_element(By.NAME, "pass")
password_field.send_keys("Mycard@123")

# Submit the login form
password_field.send_keys(Keys.RETURN)

driver.get("http://localhost:8000/LibrarianAddBook")

# Fill in the form fields
book_name = driver.find_element(By.NAME, 'book_name')
book_name.send_keys('The Catcher in the Rye')
time.sleep(2)

category = Select(driver.find_element(By.NAME, 'category'))
category.select_by_value('5')
time.sleep(2)

book_language = driver.find_element(By.NAME, 'book_language')
book_language.send_keys('English')
time.sleep(2)

book_author = driver.find_element(By.NAME, 'book_author')
book_author.send_keys('J.D. Salinger')
time.sleep(2)

book_desc = driver.find_element(By.NAME, 'book_desc')
book_desc.send_keys('A novel about a teenage boy dealing with alienation and disillusionment')
time.sleep(2)

book_year = driver.find_element(By.NAME, 'book_year')
book_year.send_keys('1951')
time.sleep(2)

book_publisher = driver.find_element(By.NAME, 'book_publisher')
book_publisher.send_keys('Little, Brown and Company')
time.sleep(2)

image_upload = driver.find_element(By.NAME, "img")
image_upload.send_keys(r"D:\PROJECT\MycardProjectect\static\images\pics\catcherbook.jpg")
time.sleep(2)

book_price = driver.find_element(By.NAME, 'book_price')
book_price.send_keys('150')
time.sleep(2)

isbn = driver.find_element(By.NAME, 'isbn')
isbn.send_keys('0316769487')
time.sleep(2)

book_quantity = driver.find_element(By.NAME, 'book_quantity')
book_quantity.send_keys('10')
time.sleep(2)


# Submit the form
submit_button = driver.find_element('css selector', 'button[type="submit"]')
submit_button.click()
time.sleep(2)
driver.get("http://127.0.0.1:8000/booktable")
time.sleep(5)

# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h3[contains(text(), 'Books')]")
if dashboard_element:
    print("Book Add Successfull")
else:
    print("Test failed.")





