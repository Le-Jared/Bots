from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import chromedriver_binary
import random
import time
import pandas as pd

# Function to simulate random wait times
def random_wait(min=5.0, max=15.0):
    wait_time = random.uniform(min, max)
    print(wait_time)
    time.sleep(wait_time)

def check_for_stock(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find("div", {"class": "items-grid-view"})
    items_processed = []

    for row in items.findAll("div", {"class": "item-cell"}):
        row_processed = []
        item_title = row.find("a", {"class": "item-title"})
        item_promo_text = row.find("p", {"class": "item-promo"})
        item_price = row.find("li", {"class": "price-current"})

        status = "Available"
        if item_promo_text and item_promo_text.text == "OUT OF STOCK":
            status = "Sold Out"

        if item_title:
            row_processed.append(item_title.text)
            row_processed.append(item_price.find("strong").text)                
            row_processed.append(item_title.get("href"))
            row_processed.append(status)

        if row_processed:
            items_processed.append(row_processed)

    df = pd.DataFrame(items_processed, columns=["Item Title","Item Price","URL","Status"])
    df["Item Price"] = df["Item Price"].apply(lambda x: x.replace(",",""))
    df["Item Price"] = pd.to_numeric(df["Item Price"])

    return df

def buy_item(url):
    driver.get(url)
    add_to_cart_button = driver.find_element_by_xpath('//*[@id="ProductBuy"]/div/div[2]/button')
    add_to_cart_button.click()
    random_wait()

    no_thanks_button = driver.find_element_by_xpath('//*[@id="modal-intermediary"]/div/div/div/div[3]/button[1]')
    no_thanks_button.click()
    random_wait()

    view_cart_button = driver.find_element_by_xpath('//*[@id="modal-intermediary"]/div/div/div[2]/div[2]/button[2]')
    view_cart_button.click()
    random_wait()

    secure_checkout_button = driver.find_element_by_xpath('//*[@id="app"]/div[1]/section/div/div/form/div[2]/div[3]/div/div/div[3]/div/button')
    secure_checkout_button.click()
    random_wait()

    guest_checkout_button = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[1]/form[2]/div[2]/div/button')
    guest_checkout_button.click()
    random_wait()

    add_address = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div/form/div[2]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/i')
    add_address.click()
    random_wait()

    # Further checkout process here

def check_and_buy(url):
    while True:
        items = check_for_stock(url)  
        in_stock = items[(items["Item Price"]< 2500) & (items.Status == "Available")]
        if not in_stock.empty:
            item_to_purchase = in_stock.iloc[0]
            buy_item(item_to_purchase["URL"])
            break
        else:
            time.sleep(120)

# Set up the webdriver and open the page
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# Specify the URL of the product
url = "https://www.newegg.com/p/pl?N=100007709%20601357282"

# Call the main function
check_and_buy(url)

# Close the browser once done
driver.quit()

