import requests
import json
import csv
from datetime import datetime

# API endpoint to get balance for a bitcoin address
balance_url = "https://blockchain.info/balance?active="

# API endpoint to get current price of BTC/USD
price_url = "https://api.coindesk.com/v1/bpi/currentprice.json"

# Bitcoin addresses
addresses = ["34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo", "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97",
             "3JJmF63ifcamPLiAmLgG96RA599yNtY3EQ","3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6",
             "1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd"]

# Fetch balance for each address
balances = []
for address in addresses:
    try:
        response = requests.get(balance_url + address)
        data = response.json()
        balance = data[address]["final_balance"] / 100000000
        balances.append(balance)
    except:
        print("Error fetching balance for " + address)

# Fetch current BTC/USD price
try:
    response = requests.get(price_url)
    data = response.json()
    usd_price = float(data["bpi"]["USD"]["rate"].replace(",", ""))
except:
    print("Error fetching current BTC/USD price")

# Print balances and USD values to console
print("Address, Balance, Value in USD")
for i in range(len(addresses)):
    if i < len(balances):
        usd_value = round(balances[i] * usd_price, 2)
        print(addresses[i] + ", " + str(balances[i]) + ", " + str(usd_value))
    else:
        print(addresses[i] + ", N/A, N/A")

# Write balances and USD values to CSV file
filename = "bitcoin_balances_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Address", "Balance", "Value in USD"])
    for i in range(len(addresses)):
        if i < len(balances):
            usd_value = round(balances[i] * usd_price, 2)
            writer.writerow([addresses[i], balances[i], usd_value])
        else:
            writer.writerow([addresses[i], "N/A", "N/A"])

