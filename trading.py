import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Do A
# python3 -m pip install python-dotenv
# python3 -m pip install intrinio-sdk

api_key = os.getenv('API_KEY')
public_key = os.getenv('PUBLIC_KEY')
header_public_key = "X-Authorization-Public-Key"

stock_list = {
	"MSFT": [64,159],
	"VZ": [40,59.82],
	"KO": [22,53.19],
	"DIS": [22,100],
	"JNJ": [12,133],
	"WDC": 30,
	"GLPI": 46,
	"SBUX": 40,
	"VOO": 10,
	"ABBV": 22,
	"T": 40
}

def get_dividend_amount():
	print("stock   dividend_paid    pay_date    monthly_x_shares    yearly_x_4")

	monthly_earned = 0
	yearly = 0

	for key in stock_list:
		try:	
			# Get requests for stock
			final_url = "https://api-v2.intrinio.com/securities/{}/dividends/latest?api_key={}".format(key,api_key)
			r = requests.get(final_url, headers={header_public_key: public_key})

			# Store in json 
			json_data = r.json()

			stock_dividend_paid = json_data['ex_dividend']
			stock_dividend_paydate = json_data['pay_date']

			monthly_x_shares = round(stock_dividend_paid * stock_list[key][0])
			monthly_earned = monthly_earned + monthly_x_shares

			yearly_earned = round(monthly_x_shares * 4)
			yearly = yearly + yearly_earned

			print(key,stock_dividend_paid,stock_dividend_paydate,monthly_x_shares,yearly_earned)
		except Exception as e:
			print("Could not find stock in the database for {} \n".format(key))

	print("Amount that could be earned monthly = {}".format(monthly_earned))
	print("Amount that could be earned yearly = {}".format(yearly))

def get_net_profit_loss():
	for key in stock_list:

		try:
			# Get requests for stock
			final_url = "https://api-v2.intrinio.com/securities/{}/prices/realtime?api_key={}".format(key,api_key)
			r = requests.get(final_url, headers={header_public_key: public_key})

			# Store in json 
			json_data = r.json()

			last_stock_price = json_data['last_price']
			net_profit_loss = abs(last_stock_price)-abs(stock_list[key][1])
			
			overall_net = net_profit_loss*stock_list[key][0]
			print("Net profit/loss for {} is {}".format(key,overall_net))
		except Exception as e:
			print("Could not find stock in the database for {} \n".format(key))

if __name__ == '__main__':
	get_dividend_amount()
	get_net_profit_loss()

