#!/usr/bin/env python
# coding: utf-8

# In[2]:


from binance.client import Client
from binance.enums import *
import time

# Set up your Binance API key and secret
api_key = ''
api_secret = ''

# Set up the client for the Binance Futures environment
client = Client(api_key, api_secret)

# Define the symbol you want to trade (e.g., 'BTCUSDT')
symbol = 'ETHUSDT'

# Define the strike price and quantity you want to trade
strike_price = '1750'
qty = '1'

# Define a function to place a market long order
def place_long_order(price, qty):
    order = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        type=ORDER_TYPE_MARKET,
        quantity=qty)
    return order

# Check if there is already an existing long position
positions = client.futures_position_information(symbol=symbol)
for position in positions:
    if position['positionSide'] == 'LONG':
        print('There is already a long position open')
        long_order_id = position['orderId']
        break
else:
    long_order_id = None

# Main loop to monitor the market price and place/close long positions as needed
while True:
    # Check the current price and place a long order if the price is greater than the strike price
    ticker = client.futures_ticker(symbol=symbol)
    current_price = float(ticker['lastPrice'])
    if float(strike_price) <= current_price and long_order_id is None:
        long_order = place_long_order(strike_price, qty)
        long_order_id = long_order['orderId']
        print(f'Long position opened at price {current_price} with quantity {qty}')

    # Check if the current price is below the strike price and there is an existing long position
    if current_price < float(strike_price) and long_order_id is not None:
        # Close the long position
        close_order = client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type=ORDER_TYPE_MARKET,
            quantity=qty)
        long_order_id = None
        print(f'Long position closed at price {current_price}')

    # Wait for 1 second before checking the price again
    time.sleep(1)


# In[ ]:




