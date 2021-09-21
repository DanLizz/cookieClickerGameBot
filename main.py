from selenium import webdriver
import time

chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get('http://orteil.dashnet.org/experiments/cookie/')

# Cookie element to click
cookie = driver.find_element_by_id("cookie")

# Upgrade items
shop = driver.find_elements_by_css_selector("#store div")
shop_items_ids = [item.get_attribute("id") for item in shop]

# Define timeout
five_sec = time.time() + 5
timeout = time.time() + 60 * 5  # 5 minutes from now

while True:
    # Click cookie
    cookie.click()

    # Every 5 seconds interval
    if time.time() > five_sec:

        # Get current money/ cookie count
        money = driver.find_element_by_id("money").text
        if "," in money:
            money = money.replace(",", "")
        money = int(money)

        # Getting tags for store items
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []

        # Store prices
        # Converting <b> text into integer price

        for price in all_prices:
            element = price.text
            if element != "":
                cost = int(element.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Dictionary of store items and prices
        cookie_upgrade = {}
        for n in range(len(item_prices)):
            cookie_upgrade[item_prices[n]] = shop_items_ids[n]

        # Affordable upgrades
        affordable_items = {}

        for cost, id in cookie_upgrade.items():
            if money > cost:
                affordable_items[cost] = id

        # Purchase most expensive affordable item

        expensive_item = max(affordable_items)
        purchase_id = affordable_items[expensive_item]

        driver.find_element_by_id(purchase_id).click()

        # Add 5 sec interval
        five_sec = time.time() + 5

    # Stop bot after 5 minutes
    if time.time() > timeout:
        cookie_per_sec = driver.find_element_by_id("cps").text
        print(cookie_per_sec)
        break
    cookie.click()
