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
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

def make_product_key(name, store_id):
  return f"{store_id}:{name.lower().strip()}"

def get_day():
  return datetime.utcnow().date()

def get_or_create_product(cur, name, store_id):
  key = make_product_key(name, store_id)

  cur.execute(
    """
    SELECT id FROM "Product"
    WHERE key = %s
    """,
    (key,)
  )

  if row := cur.fetchone():
    return row[0]

  cur.execute(
    """
    INSERT INTO "Product" (name, key)
    VALUES (%s, %s)
    RETURNING id
    """,
    (name, key)
  )

  return cur.fetchone()[0]


def save_to_db(name, price, store_id):
  conn = psycopg.connect(DATABASE_URL)
  cur = conn.cursor()

  product_id = get_or_create_product(cur, name, store_id)

  day = get_day()

  cur.execute(
    """
    INSERT INTO "Price" (price, "productId", "storeId", day)
    VALUES (%s, %s, %s, %s)
    """,
    (price, product_id, store_id, day)
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
    WHERE p.name ILIKE %s
    ORDER BY pr."createdAt" DESC
    """,
    (f"%{query}%",)
  )

  rows = cur.fetchall()

  cur.close()
  conn.close()

  return [
    {"name": r[0], "price": r[1]}
    for r in rows
  ]