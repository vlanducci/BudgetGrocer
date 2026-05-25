from scraper import aldi, coles, woolworths
from db import save_to_db

def scrape_job(item):
    aldi_name, aldi_price = aldi()
    coles_name, coles_price = coles()
    wool_name, wool_price = woolworths()

    save_to_db(aldi_name, aldi_price, "Aldi")
    save_to_db(coles_name, coles_price, "Coles")
    save_to_db(wool_name, wool_price, "Woolworths")

    return True