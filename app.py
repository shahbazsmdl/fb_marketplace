from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import shutil
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv

# Set up headless browsing options
chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

# Set up Chrome webdriver with headless options and Permissions-Policy header
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_experimental_option("prefs", {
  "profile.default_content_setting_values.notifications": 2,
  "profile.default_content_setting_values.media_stream_camera": 2,
  "profile.default_content_setting_values.media_stream_mic": 2,
})
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("Permissions-Policy=interest-cohort=()")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com/")


FB_USERNAME=""
FB_PASSWORD=""
def marketplace_share():
  # Open the CSV file and read the data
  with open('Marketplace Data sharing - Sheet1.csv', 'r') as file:
      reader = csv.reader(file)
      rows = list(reader)
  all_published=True
  # Process the data and update the status column
  for i in range(1, len(rows)):
      if not rows[i][5] or rows[i][5].strip().lower() != 'published':
          # Update the status column to 'published'
          all_published=False
          title=rows[i][0]
          description=rows[i][1]
          price=rows[i][2]
          link=rows[i][3]
          location=rows[i][4]
          rows[i][5] = 'published'
          break
  if all_published:
      print("All rows are already published.")
      exit()
  print('Done')
  # Download the image from the Google Drive link
  id_start = link.find('/d/') + 3
  id_end = link.find('/view')
  file_id = link[id_start:id_end]
  print(file_id)
  driver.get(f"https://www.facebook.com/marketplace/create/item")
  time.sleep(3)
  response = requests.get(f"https://drive.google.com/uc?id={file_id}", stream=True)
  with open("image.jpg", "wb") as out_file:
      shutil.copyfileobj(response.raw, out_file)
  del response
  # Upload the image to Facebook Marketplace
  file_input = driver.find_element(By.XPATH, "//input[@type='file']")
  file_input.send_keys(os.path.abspath("image.jpg"))
  time.sleep(5)
  # Find the input field for title and enter the text
  title_input = driver.find_element(By.ID, ":rs:")
  # Set the value of the input element to "hi this my title"
  title_input.send_keys(title)
  time.sleep(2)
  price_input = driver.find_element(By.ID,':ru:')
  price_input.send_keys(price)
  time.sleep(2)
  # Find the category dropdown element
  category_dropdown = driver.find_element(By.XPATH, "//label[@for=':r10:']")
  # Click on the dropdown element to open the options
  category_dropdown.click()
  time.sleep(2)
  # Find the furniture category option by its text
  furniture_option = driver.find_element(By.XPATH ,"//span[contains(text(), 'Furniture')]")
  # Click on the furniture option to select it
  furniture_option.click()
  time.sleep(2)
# Find the category dropdown element
  condition_dropdown = driver.find_element(By.XPATH, "//label[@for=':r14:']")
  condition_dropdown.click()
  time.sleep(2)
  new_option = driver.find_element(By.XPATH ,"//span[contains(text(), 'New')]")
  new_option.click()
  # time.sleep(5)
  # more_details_button = driver.find_element(By.XPATH ,'//span[text()="More Details"]')
  # more_details_button.click()
  time.sleep(5)
  # Find the label element by its text
  label_element = driver.find_element(By.XPATH, "//span[text()='Description']")
  # Find the parent element of the label element
  parent_element = label_element.find_element(By.XPATH, "..")
  # Find the textarea element within the parent element
  textarea_element = parent_element.find_element(By.TAG_NAME, "textarea")
  textarea_element.send_keys(description)
  time.sleep(10)
  # find the location input field
  location_input = driver.find_element(By.XPATH, "//input[@aria-label='Enter a city']")
  # clear the current value of the field
  location_input.send_keys(Keys.CONTROL, "a")
  location_input.send_keys(Keys.DELETE)
  # set the new value to "Manchester"
  location_input.send_keys(location)
  time.sleep(5)
  suggestions_list = driver.find_element(By.XPATH,"//ul[@aria-label='5 suggested searches']")
  time.sleep(2)
  first_suggestion = suggestions_list.find_element(By.XPATH,"./li[1]")
  first_suggestion.click()
  time.sleep(5)
  # Wait for the checkbox to become clickable
  checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Door dropoff']/../..")))
  # Click the checkbox
  checkbox.click()
  next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
  next_button.click()
  publis_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Publish']")))
  publis_button.click()
  # Update the last column of the first row with the value "publish"
  # Write the updated data back to the CSV file
  with open('Marketplace Data sharing - Sheet1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)



email = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email")))
# Find password field and fill them in
password = driver.find_element(By.ID, "pass")
email.send_keys(FB_USERNAME)
password.send_keys(FB_PASSWORD)

time.sleep(2)

login_button = driver.find_element(By.XPATH, "//button[contains(., 'Log in')]")
login_button.click()
# # this const
time.sleep(5)

#marketplace share
while True:
  marketplace_share()
  time.sleep(5)
driver.quit()
