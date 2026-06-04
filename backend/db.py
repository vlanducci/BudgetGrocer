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

def get_or_create_product(cur, name):
  cur.execute(
    """
    SELECT id FROM "Product"
    WHERE LOWER(name) = LOWER(%s)
    """,
    (name,)
  )

  if row := cur.fetchone():
    return row[0]

  cur.execute(
    """
    INSERT INTO "Product" (name)
    VALUES (%s)
    RETURNING id
    """,
    (name,)
  )

  return cur.fetchone()[0]


def save_to_db(name, price, store_id):
  conn = psycopg.connect(DATABASE_URL)
  cur = conn.cursor()

  product_id = get_or_create_product(cur, name)

  cur.execute(
    """
    INSERT INTO "Price" (price, "productId", "storeId")
    VALUES (%s, %s, %s)
    """,
    (price, product_id, store_id)
  )

  conn.commit()
  cur.close()
  conn.close()

def get_from_db(query):
  conn = psycopg.connect(DATABASE_URL)
  cur = conn.cursor()

  cur.execute(
    """
    SELECT p.name, pr.price
    FROM "Product" p
    JOIN "Price" pr ON pr."productId" = p.id
    WHERE LOWER(p.name) = LOWER(%s)
    ORDER BY pr."createdAt" DESC
    """,
    (query,)
  )

  rows = cur.fetchall()

  cur.close()
  conn.close()

  return [
    {"name": r[0], "price": r[1]}
    for r in rows
  ]