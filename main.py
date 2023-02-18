from aiohttp import ClientSession
import asyncio
import numpy as np
from datetime import datetime

#_______________#states#_____________#states#_____________#states#_____________#states#_____________#states#
state_url = 'https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-product-by-symbol?symbol='
state_symbol_BTC = 'BTCUSDT'
state_symbol_ETH = 'ETHUSDT'
start_time = datetime.now()
hour = 3600
state_price = None
BTC_USDT = []
ETH_USDT = []
X_line = "-"*14
W_line = " "*6
starting = True


async def check_correlation():
	if len(BTC_USDT) >= 100:
		correlate = np.corrcoef(BTC_USDT, ETH_USDT)
		result = correlate[0][1]
		BTC_USDT.clear()
		ETH_USDT.clear()
		return result
	return None


async def check_time(price):
	global start_time
	if (datetime.now() - start_time).total_seconds() >= hour:
		start_time = datetime.now()
		return await check_out(price=price)
	return


async def check_out(price):
	alert = ((float(state_price) - float(price))/float(state_price))*100
	if (alert >= 1) or float(state_price)*0.99 >= float(price):
		print(f'IT\'S ALLERT!!!======================= Price changed at {alert}% =======================')
	return


async def check_price_live(price, btc):
	global state_price
	global starting
	starting = True
	# BTC_USDT.append(float(btc))
	# ETH_USDT.append(float(price))
	if state_price is None:
		state_price = price
	correlation = 0.8138748188334043 #await check_correlation() - было занесено 100 значений
	# if correlation is None:
	# 	correlation = 0
	real_eth = (float(correlation) * float(price))
	print(f"{X_line*10}\nBTC: {btc}{W_line}ETH: {price}{W_line}CORRELATION: {correlation}{W_line}Real ETH: {real_eth}\n{X_line*10}")
	await check_time(price=price)


async def main():
	global starting
	while starting:
		starting = False
		async with ClientSession() as session:
			async with session.get(state_url + state_symbol_BTC) as dataBTC:
				dataBTC = await dataBTC.json()
				async with session.get(url=state_url + state_symbol_ETH) as dataETH:
					dataETH = await dataETH.json()
					await check_price_live(price=dataETH['data']['c'], btc=dataBTC['data']['c'])

if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(main())