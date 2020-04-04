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
	"MSFT": 64,
	"VZ": 40,
	"KO": 22,
	"DIS": 22,
	"JNJ": 12,
	"WDC": 30,
	"GLPI": 46,
	"SBUX": 40,
	"VOO": 10,
	"ABBV": 22,
	"T": 40
}

print("stock   dividend_paid  pay_date monthly_x_shares  yearly_x_4 ")

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

		monthly_x_shares = round(stock_dividend_paid * stock_list[key])
		monthly_earned = monthly_earned + monthly_x_shares

		yearly_earned = round(monthly_x_shares * 4)
		yearly = yearly + yearly_earned

		print(key,stock_dividend_paid,stock_dividend_paydate,monthly_x_shares,yearly_earned)
	except Exception as e:
		print("Could not find stock in the database for {}".format(key))

print(monthly_earned)
print(yearly)

