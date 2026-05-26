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

DATABASE_URL = os.getenv("DATABASE_URL")

def save_to_db(name, price, store):
  conn = psycopg.connect(DATABASE_URL)
  cur = conn.cursor()
  
  item = "tomato"  # temp

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
