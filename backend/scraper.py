from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains

import psycopg
import os
from dotenv import load_dotenv
import asyncio
import time
import re


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def create_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument("--window-size=1920,1080")
  options.add_argument("--disable-blink-features=AutomationControlled")
  options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--disable-gpu")
  # options.binary_location = "/usr/bin/chromium"

  return uc.Chrome(options=options, version_main=148)

def aldi(driver, item):
  aldi_items = []

  # Load the URL
  aldi_url = f"https://www.aldi.com.au/results?q={item}"
  driver.get(aldi_url)

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 15)

  wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "a.product-tile__link")) > 0)

  wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.product-tile__link"))
  )

  products = driver.find_elements(By.CSS_SELECTOR, "a.product-tile__link")

  for product in products[0:1]:
    # find price element inside shadow DOM
    price = product.find_element(By.CLASS_NAME, "base-price__regular")

    # find name element inside shadow DOM
    name = product.find_element(By.CLASS_NAME, "product-tile__name")

    aldi_items.append((name.text, price.text))
  
  aldi_cheapest = min(aldi_items, key=lambda x: x[1])
  return aldi_cheapest

def coles(driver, item):
  coles_items = []

  # Load the URL
  coles_url = f"https://www.coles.com.au/search/products?q={item}"
  driver.get(coles_url)
  print(driver.page_source[:1000])

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 15)

  wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='product-tile']")))


  products = driver.find_elements(By.CSS_SELECTOR, "a[href*='/product/']")

  for product in products[0:2]:  
    # find price element inside shadow DOM
    price = product.find_element(By.CLASS_NAME, "price__value")

    # find name element inside shadow DOM
    name = product.find_element(By.CLASS_NAME, "product__title")

    coles_items.append((name.text, price.text))

  coles_cheapest = min(coles_items, key=lambda x: x[1])
  return coles_cheapest

def woolworths(driver, item):
  woolworths_items = []

  # Load the URL
  woolworths_url = f"https://www.woolworths.com.au/shop/search/products?searchTerm={item}"
  driver.get(woolworths_url)

  # Optional wait to ensure page loads
  wait = WebDriverWait(driver, 30)

  wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "wc-product-tile")) > 0)

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