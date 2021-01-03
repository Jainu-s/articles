# Libraries
from fyers_api import accessToken
from fyers_api import fyersModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import json
import time
import pandas as pd
import os
import glob


# GLOBAL Variables to hold data
global pending_order_id


def request_auth():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--user-data-dir = chrome-data")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path="chromdriver85/chromedriver",
                              options=options)  # , chrome_options=options)
    driver.maximize_window()

    # Authentication
    app_id = "VUJXY71KQH"
    app_secret = "Q4V3PBIKER"
    app_session = accessToken.SessionModel(app_id, app_secret)
    response = app_session.auth()

    print(response)

    # Getting authorized code into a variable
    authorization_code = response['data']['authorization_code']

    # Setting a Session
    print(app_session.set_token(authorization_code))

    access_token_url = app_session.generate_token()

    # Opening Url through Selenium
    driver.get(str(access_token_url))

    usn = driver.find_element_by_id('fyers_id')
    usn.send_keys('DJ00795')
    time.sleep(3)

    pwd = driver.find_element_by_id('password')
    pwd.send_keys('Allah@786')
    time.sleep(3)

    driver.find_element_by_class_name('login-span-pan').click()
    time.sleep(3)

    pan = driver.find_element_by_id('pancard')
    pan.send_keys('GVSPS4837L')
    time.sleep(3)

    driver.find_element_by_id('btn_id').click()

    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_is('jainusalgotradetest.in'))
    # getting access token from browser
    exclude, redirected_url = driver.current_url.split('=', 1)
    token = redirected_url
    print(token)

    # Quiting the browser
    # driver.quit()

    # token = 'gAAAAABfeL21YprsghfV2ZcAAUQI69qwAw7C5QqCXbd1PlH9WywvAbkzIAmUctKds7XULxdefnGl_zZWmxX3XjLEGf52sPgzukOTr64OVJLe4vosXMHf788=&user_id=DJ00795'

    # By default False only
    is_async = False

    fyers = fyersModel.FyersModel(is_async)

    # accessing funds data in json
    funds_data = fyers.funds(token=token)

    avail_funds = funds_data['data']['fund_limit']
    avb = pd.json_normalize(avail_funds)
    # avb.to_csv(os.getcwd() + '/availfunds/funds.csv')

    bal = float()
    if avb.iloc[0][1] > 0:
        bal = avb.iloc[0][1]


    return fyers, token , bal


def execute_orders(final_stock_name, stock_quantity, side, buy_sell_price, stop_loss):
    fyers, token, bal = request_auth()
    executed_order = fyers.place_orders(token=token, data={"symbol": "NSE:{}-EQ".format(final_stock_name),
                                                           "qty": stock_quantity,
                                                           "type": 1,
                                                           "side": side,
                                                           "productType": "BO",
                                                           "limitPrice": buy_sell_price,
                                                           "stopPrice": 0,
                                                           "disclosedQty": 0,
                                                           "validity": "DAY",
                                                           "offlineOrder": "False",
                                                           "stopLoss": stop_loss,
                                                           "takeProfit": 2
                                                           })
    print(executed_order)
    # pending_order_id = executed_order['data']['id']
    # print(pending_order_id)


# Modifying orders
def modify_orders():
    fyers, token, bal = request_auth()
    fyers.update_orders(token = token,data = {"id" : "120100673546-BO-1","type" : "1",'stopLoss':1})





# Execute this function at 11:00AM
def cancel_pending_orders():
    try:
        fyers, token, bal = request_auth()
        cancel_order = fyers.delete_orders(token=token, data={"id": '120100673546-BO-1'})

        if cancel_order['message'] == "Successfully cancelled order":
            print('Pending Orders Cancelled at 11:00 AM')
            print('Message sent to mobile')
    except:
        pass



# Exit Open Positions before 02:50 PM
def exit_open_position():
    try:
        fyers, token, bal = request_auth()
        cancel_position = fyers.exit_positions(token=token)
        print(cancel_position)
    except:
        pass

# Order Status
def order_status():

    fyers, token, bal = request_auth()
    orderstatus = fyers.order_status(token = token,data = {"id" : "119050790482"})
    print(orderstatus)





