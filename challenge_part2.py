# CoinPanel Backend Engineer Challenge part 2
# Author: ViNOJ DAViS
import websockets
import asyncio
import json
import time
import sys


async def main(symbol, monitor_price):
    """Main Program to monitor price of symbol given by user

    Args:
        symbol (str): Binance symbol for monitoring of price level
        monitor_price (float): Price level to monitor symbol
    """
    # STREAM ENDPOINT
    endpoint = "wss://stream.binance.com:9443/stream?streams=" + symbol.lower() + \
        "@miniTicker"
    async with websockets.connect(endpoint) as client:
        while True:
            data = json.loads(await client.recv())['data']

            # Formatting to localtime
            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

            last_price = float(data['c'])

            if last_price > monitor_price:
                print(event_time, symbol, "price has gone above",
                      monitor_price, "Last price:", last_price)

            # You can comment below lines if you don't want to see live price
            else:
                print(event_time, "Last price for symbol",
                      symbol, ":", last_price)


def check_price(lp):
    """ It will check if the price value given by user is a valid float

    Args:
        lp (str): User input to monitor price

    Returns:
        float: return float value of the lp if valid else exit
    """
    try:
        return float(lp)
    except:
        print("Invalid price found!! \nPlease start again..")
        sys.exit(1)


if __name__ == '__main__':
    symbol = input(
        "Enter Symbol to monitor (eg: BNBBTC,ETHBTC,BTCUSDT,ETHUSDT,etc..): ")
    monitor_price = input("Enter price to monitor " + symbol + " symbol: ")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(symbol, check_price(monitor_price)))
    except KeyboardInterrupt:
        print("\nReceived exit, exiting")
