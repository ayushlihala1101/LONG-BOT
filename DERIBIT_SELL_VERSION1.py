#!/usr/bin/env python
# coding: utf-8

# In[1]:


from binance.client import Client
import time

# Set up your Binance API key and secret
api_key = ''
api_secret = ''

# Set up the client for the Binance Futures environment
client = Client(api_key, api_secret)

# Define the symbol you want to trade (e.g., 'BTCUSDT')
symbol = 'BTCUSDT'

# Define the strike price and quantity you want to trade
strike_price = '23500'
qty = '0.10'

# Define a function to place a market short order
def place_short_order(price, qty):
    order = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='MARKET',
        quantity=qty)
    return order

# Define a function to close a short position
def close_short_position(position):
    order = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        type='MARKET',
        positionSide=position,
        quantity=qty)
    return order

# Check if there is already an existing short position
positions = client.futures_position_information(symbol=symbol)
for position in positions:
    if position['positionSide'] == 'SHORT':
        print('There is already a short position open')
        short_order_id = None
        break
else:
    short_order_id = None

# Main loop to monitor the market price and place/close short positions as needed
while True:
    # Check the current price and place a short order if the price is less than the strike price
    ticker = client.futures_ticker(symbol=symbol)
    current_price = float(ticker['lastPrice'])
    if float(strike_price) > current_price and short_order_id is None:
        short_order = place_short_order(strike_price, qty)
        short_order_id = short_order['orderId']
        position = short_order['positionSide']
        print(f'Short position opened at price {strike_price} with quantity {qty}')

    # Close the short position if the current price is higher than the strike price
    ticker = client.futures_ticker(symbol=symbol)
    current_price = float(ticker['lastPrice'])
    if float(strike_price) < current_price and short_order_id is not None:
        close_short_position(position)
        print('Short position closed')
        short_order_id = None

    # Wait for 1 second before checking the price again
    time.sleep(1)


# In[ ]:




