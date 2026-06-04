from scraper import aldi, coles, woolworths, create_driver

driver = create_driver()

# aldi_name, aldi_price = aldi(driver, 'tomato')
# print(aldi_name, aldi_price)

# woolworths_name, woolworths_price = woolworths(driver, 'tomato')
# print(woolworths_name, woolworths_price)

coles_name, coles_price = coles(driver, 'tomato')
print(coles_name, coles_price)

