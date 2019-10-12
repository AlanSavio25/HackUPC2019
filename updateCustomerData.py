import json
from pprint import pprint
with open('customerData.json') as f:
   customerData = json.load(f)


with open('dailyReport.json') as f:
   dailyData = json.load(f)

customerData[dailyData["custID"]][dailyData["day"]].append(dailyData["trips"])

pprint(customerData)
with open('customerData.json', 'w') as f:
    json.dump(customerData, f)
