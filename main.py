from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


options = webdriver.ChromeOptions()
driver = uc.Chrome()

woolworths_url = f"https://www.woolworths.com.au/"
coles_url = f"https://www.coles.com.au/"

item = "cherry tomato"

# temp = input("1 or 2: ")
temp = "2"

if temp == "1": 
  # Load the URL
  driver.get(coles_url)

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 15)

  # wait for search to load
  search = wait.until(EC.element_to_be_clickable((By.ID, "search-text-input")))
  driver.execute_script("arguments[0].focus();", search)

  search = driver.find_element(By.ID, "search-text-input")

  search.send_keys(item)
  driver.switch_to.active_element.send_keys(Keys.ENTER)

  sort = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiInputBase-root.MuiInput-root.MuiInput-underline.MuiInputBase-colorPrimary.MuiInputBase-formControl.MuiSelect-root.css-vrsrqt")))
  sort.click()

  low = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='relevance']")))
  low.click()

  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product-tile']")))

  time.sleep(1)

  products = driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-tile']")

  for product in products:  
    # find price element inside shadow DOM
    price = product.find_element(By.CLASS_NAME, "price__value")

    # find name element inside shadow DOM
    name = product.find_element(By.CLASS_NAME, "product__title")

    print(name.text)
    print(price.text)

else:
  # Load the URL
  driver.get(woolworths_url)

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 15)

  # wait for search to load
  search = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']")))

  search.click()

  search.send_keys(item)

  search.send_keys(Keys.ENTER)

  # sort = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".chip.chip-menu.chip-secondary")))
  # sort.click()

  # low = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".wowRadio-label[for='singleSelectionMenuItem-5']")))
  # low.click()

  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "wc-product-tile")))
  time.sleep(1)

  products = driver.find_elements(By.CSS_SELECTOR, "wc-product-tile")
  
  for product in products:
    # find shadow root - entry root to a shadow DOM - a web standard that allows you to attach a hidden, separate DOM tree to an element, providing encapsulation for its structure and styles
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", product)

    # find price element inside shadow DOM
    price = shadow_root.find_element(By.CLASS_NAME, "primary")

    # find name element inside shadow DOM
    name = shadow_root.find_element(By.CLASS_NAME, "title")

    print(name.text)
    print(price.text)

  time.sleep(10)