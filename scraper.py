from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import psycopg
import os
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

options = webdriver.ChromeOptions()
driver = uc.Chrome(version_main=148)

item = "tomato"

def save_to_db(name, price, store):
  conn = psycopg.connect(DATABASE_URL)
  cur = conn.cursor()

  cur.execute(
    """
    INSERT INTO "Product" (query, data)
    VALUES (%s, %s)
    """,
    (
      item,
      {
        "name": name,
        "price": price,
        "store": store
      }
    )
  )

  conn.commit()
  cur.close()
  conn.close()

def aldi():
  aldi_items = []
  # Load the URL
  aldi_url = f"https://www.aldi.com.au/"
  driver.get(aldi_url)

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 15)

  # wait for search to load
  search = wait.until(EC.element_to_be_clickable((By.ID, "search-bar-input")))

  search.click()

  search.send_keys(item)
  time.sleep(1)

  search.send_keys(Keys.ENTER)

  wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-grid")))
  time.sleep(1)

  products = driver.find_elements(By.CSS_SELECTOR, "a.product-tile__link")

  for product in products[0:1]:
    # find price element inside shadow DOM
    price = product.find_element(By.CLASS_NAME, "base-price__regular")

    # find name element inside shadow DOM
    name = product.find_element(By.CLASS_NAME, "product-tile__name")

    aldi_items.append((name.text, price.text))
  
  aldi_cheapest = min(aldi_items, key=lambda x: x[1])
  return aldi_cheapest
  # print(f"Cheapest item at Aldi: {aldi_cheapest[0]} for {aldi_cheapest[1]}")

def coles():
  coles_items = []

  # Load the URL
  coles_url = f"https://www.coles.com.au/"
  driver.get(coles_url)

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 15)

  # wait for search to load
  button = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='search-box-search-button']"))
  )

  driver.execute_script("arguments[0].click();", button)

  search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-box-select__input")))

  search.send_keys(item)
  time.sleep(1)

  search.send_keys(Keys.ENTER)

  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product-tile']")))

  time.sleep(1)

  products = driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-tile']")

  for product in products[0:2]:  
    # find price element inside shadow DOM
    price = product.find_element(By.CLASS_NAME, "price__value")

    # find name element inside shadow DOM
    name = product.find_element(By.CLASS_NAME, "product__title")

    coles_items.append((name.text, price.text))

  coles_cheapest = min(coles_items, key=lambda x: x[1])
  return coles_cheapest
  # print(f"Cheapest item at Coles: {coles_cheapest[0]} for {coles_cheapest[1]}")

def woolworths():
  woolworths_items = []

  # Load the URL
  woolworths_url = f"https://www.woolworths.com.au/"
  driver.get(woolworths_url)

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 15)

  # wait for search to load
  search = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']")))

  search.click()

  search.send_keys(item)
  time.sleep(1)

  search.send_keys(Keys.ENTER)

  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "wc-product-tile")))
  time.sleep(1)

  products = driver.find_elements(By.CSS_SELECTOR, "wc-product-tile")

  for product in products[0:2]:
    # find shadow root - entry root to a shadow DOM - a web standard that allows you to attach a hidden, separate DOM tree to an element, providing encapsulation for its structure and styles
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", product)

    # find price element inside shadow DOM
    price = shadow_root.find_element(By.CLASS_NAME, "primary")

    # find name element inside shadow DOM
    name = shadow_root.find_element(By.CLASS_NAME, "title")

    woolworths_items.append((name.text, price.text))
  
  woolworths_cheapest = min(woolworths_items, key=lambda x: x[1])
  return woolworths_cheapest
  # print(f"Cheapest item at Woolworths: {woolworths_cheapest[0]} for {woolworths_cheapest[1]}")

async def main():
  aldi_name, aldi_price = aldi()
  coles_name, coles_price = coles()
  wool_name, wool_price = woolworths()

  save_to_db(aldi_name, aldi_price, "Aldi")
  save_to_db(coles_name, coles_price, "Coles")
  save_to_db(wool_name, wool_price, "Woolworths")

  driver.quit()


if __name__ == "__main__":
  asyncio.run(main())
