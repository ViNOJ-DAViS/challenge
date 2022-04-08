import websockets
import asyncio
import json
from datetime import datetime
from time import sleep, localtime
import pandas as pd
import _pickle as cpickle

my_socket = "wss://stream.binance.com:9443/ws/!ticker@arr"

picklefname = datetime.now().strftime("%Y%m%d_%H%M%S") + ".pickle"

market_data = {}


async def wclient():
    """Main Web socket client to received data asynchronously
    """
    while True:
        try:
            async with websockets.connect(my_socket) as ws:
                while True:
                    await on_message(await ws.recv())
        except Exception as e:
            await asyncio.sleep(5)


async def on_message(message):
    """This function handles raw data from Websocket

    Args:
        message (string): raw data from websocket
    """
    message_json = json.loads(message)
    # print("Total Msg Length:", len(message_json))

    for msg in message_json:
        # msg['E'] = localtime(msg['E'] // 1000)
        if msg["s"] in market_data.keys():
            market_data[msg["s"]] = pd.concat(
                [market_data[msg["s"]], pd.DataFrame(msg, index=[0])], ignore_index=True)
        else:
            market_data[msg["s"]] = pd.DataFrame(msg, index=[0])
        # market_data[msg["s"]] = market_data[msg["s"]].set_index('E')

    print(datetime.now().strftime("%H:%M:%S"),
          "Total Symbols recorderd:", len(market_data.keys()))


def save_market_data_in_pickle(market_data):
    """Save all symbol data in pickle

    Args:
        market_data (dict): This will have all market data from the Binance
    """
    for data in market_data:
        market_data[data]["E"] = pd.to_datetime(
            market_data[data]["E"], unit='ms')
        market_data[data] = market_data[data].set_index('E')

    with open(picklefname, 'wb') as fh:
        cpickle.dump(market_data, fh)

    print("Total no. of symbol data saved in file '" +
          picklefname + "':", len(market_data.keys()))


def save_market_data_in_excel(market_data):
    """Save all symbol data in an excel file

    Args:
        market_data (dict): This will have all market data from the Binance.
    """
    #
    writer = pd.ExcelWriter(
        'BINANCE-' + datetime.now().strftime("%m%d%Y_%H%M%S") + '.xlsx', engine='xlsxwriter')
    for each in market_data.keys():
        market_data[each].to_excel(
            writer, sheet_name=str(each))
    writer.save()


loop = asyncio.get_event_loop()
wclient = loop.create_task(wclient())

try:
    loop.run_forever()
except KeyboardInterrupt:
    wclient.cancel()
    print("\nReceived exit, exiting")
    print("saving data")
    # save_market_data_in_excel(market_data) # not recommended for large data
    save_market_data_in_pickle(market_data)
