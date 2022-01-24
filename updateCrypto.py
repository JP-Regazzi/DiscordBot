import asyncio
import time

from replit import db
import os

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    'slug':'bitcoin,ethereum,thetan-coin,thetan-arena',
    'convert':'USD' # Can be BRL
}
headers = {
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY': os.environ['CoinMarketCap']
}
session = Session()
session.headers.update(headers)

def cryptoRequest():
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)['data']

    BTCDATA = data['1']['quote']['USD']
    ETHDATA = data['1027']['quote']['USD']
    THCDATA = data['15250']['quote']['USD']
    THGDATA = data['11926']['quote']['USD']

    lastUpdate = 'Last updated: ' + BTCDATA["last_updated"][:10] + ' 0' + str(int(BTCDATA["last_updated"][11:13]) - 3) + BTCDATA["last_updated"][13:19]

    db["BTCDATA"] = BTCDATA
    db["ETHDATA"] = ETHDATA
    db["THCDATA"] = THCDATA
    db["THGDATA"] = THGDATA
    db["lastUpdate"] = lastUpdate
    
    print(db["lastUpdate"])
    print(f'BTC price: ${db["BTCDATA"]["price"]}')
    print(f'ETH price: ${db["ETHDATA"]["price"]}')
    print(f'THC price: ${db["THCDATA"]["price"]}')
    print(f'THG price: ${db["THGDATA"]["price"]}\n')

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

async def looping():
  while True: # not client.is_closed()
    try:
      await asyncio.sleep(20)
      cryptoRequest()
      updateAlarm()
      await asyncio.sleep(240)
    except Exception as e:
      print(e)
      await asyncio.sleep(180)


def updateAlarm():
  print("updating Alarms")
  if (db["THCDATA"]["percent_change_24h"] >= 5.0) or (db["THGDATA"]["percent_change_24h"] >= 5.0): # Liga se acima de algo
    if not db["GreenAlert"]:
      db["GreenAlert"] = True
  else: # Desliga se desceu novamente
    if db["GreenAlert"]:
      db["GreenAlert"] = False
  if (db["THCDATA"]["percent_change_24h"] <= -5.0) or (db["THGDATA"]["percent_change_24h"] <= -5.0): # Liga se abaixo de algo
    if not db["RedAlert"]: 
      db["RedAlert"] = True
  else: # Desliga se subiu novamente
    if db["RedAlert"]:
      db["RedAlert"] = False
  print(f'Green Alert: {db["GreenAlert"]}\nRed Alert: {db["RedAlert"]}\n')
