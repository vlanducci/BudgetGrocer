from scraper import aldi, coles, woolworths, create_driver
from db import save_to_db

def scrape_job(item):
    driver = create_driver()
    aldi_name, aldi_price = aldi(driver)
    coles_name, coles_price = coles(driver)
    wool_name, wool_price = woolworths(driver)

    save_to_db(aldi_name, aldi_price, "Aldi")
    save_to_db(coles_name, coles_price, "Coles")
    save_to_db(wool_name, wool_price, "Woolworths")

    return True