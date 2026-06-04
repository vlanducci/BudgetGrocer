from scraper import aldi, coles, woolworths, create_driver
from db import save_to_db, get_or_create_product, get_from_db

def scrape_job(query): 
    existing = get_from_db(query)

    if existing:
        print("exists")
        return existing

    driver = create_driver()

    aldi_name, aldi_price = aldi(driver, query)
    # coles_name, coles_price = coles(driver, query)
    wool_name, wool_price = woolworths(driver, query)

    aldi_price = aldi_price.replace("$", "").replace(",", "").strip()
    wool_price = wool_price.replace("$", "").replace(",", "").strip()

    aldi_price = float(aldi_price)
    wool_price = float(wool_price)

    save_to_db(aldi_name, aldi_price, 1)
    # save_to_db(coles_name, coles_price, 2)
    save_to_db(wool_name, wool_price, 3)

    return get_from_db(query)