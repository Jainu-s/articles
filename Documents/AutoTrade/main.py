# Libraries
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import schedule
import time
import numpy as np
from selenium.webdriver.support.select import Select

# Importing from other functions
from fyersapi import request_auth, execute_orders, cancel_pending_orders

# #########
# #########


def cancelling_pending_orders():
    cancel_pending_orders()



def sell_trigger(final_stock_name, stock_quantity, Low, High):
    stop_loss = High - Low
    execute_orders(final_stock_name, stock_quantity, -1, Low, stop_loss)


def buy_trigger(final_stock_name, stock_quantity, High, Low):
    stop_loss = High-Low
    execute_orders(final_stock_name, stock_quantity, 1, High, stop_loss)


def quantity_calculator(bal, LTP):
    margin = 22
    margin_bal = bal * margin
    quantity = np.floor(margin_bal / LTP)

    return quantity


def scrape_one_hour_hl_prices():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="chromdriver85/chromedriver", chrome_options=options)

    driver.get("https://www.traderscockpit.com/?pageView=symbol-analysis&company=HDFC%20Bank%20Limited&symbol=HDFCBANK")
    # driver.get("https://www.traderscockpit.com/?pageView=nse-indices-stock-watch&index=NIFTY+500")

    driver.implicitly_wait(5)

    High = driver.find_element_by_id("dayHigh").text
    Low = driver.find_element_by_id("dayLow").text
    LTP = driver.find_element_by_id("closePrice").text

    driver.quit()

    return High, Low, LTP


def main():
    High, Low, LTP = scrape_one_hour_hl_prices()

    fyers, token, bal = request_auth()

    stock_quantity = quantity_calculator(bal, LTP)

    final_stock_name = "HDFCBANK"

    buy_trigger(final_stock_name, stock_quantity, High, Low)
    sell_trigger(final_stock_name, stock_quantity, Low, High)



if __name__ == '__main__':

    schedule.every().monday.at("10:16").do(main)
    schedule.every().tuesday.at("10:16").do(main)
    schedule.every().wednesday.at("10:16").do(main)
    schedule.every().thursday.at("10:16").do(main)
    schedule.every().friday.at("10:16").do(main)

    while True:
        schedule.run_pending()
        time.sleep(5)
