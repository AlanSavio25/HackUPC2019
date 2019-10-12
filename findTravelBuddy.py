import json
from pprint import pprint

def close(driver, passenger):
	dist = (driver[0]-passenger[0])**2
	dist += (driver[1]-passenger[1])**2
	if (dist<0.001):
		return True
	else:
		return False

def matchingEndTime(driver,passenger):
	diff = abs(driver-passenger)
	if (diff<20):
		return True;
	else:
		return False;



def updateTravelBuddy():
	with open('customerData.json') as f:
	   customerData = json.load(f)

	with open('travelBuddy.json') as e:
	   travelBuddy = json.load(e)
	for driver in customerData.keys():
		for day in customerData[driver].keys():
			for trip in customerData[driver][day]:
				for passenger in customerData.keys():
					for trip2 in customerData[passenger][day]:
						if(close(trip["stopPlace"],trip2["stopPlace"]) and matchingEndTime (trip["stopTime"],trip2["stopTime"]) and (driver!=passenger)):
							delay = 0;#calculate
							if delay<20:
								print(trip)
								print(travelBuddy['wednesday'])
								print("hello")
								print(trip["stopTime"])
								travelBuddy[day].append({"driver":driver,"passenger":passenger, "destTime":int(trip["stopTime"]), "destLoc": trip["stopPlace"], "delay": delay})

	#pprint(travelBuddy)#
	with open('travelBuddy.json', 'w') as f:
		json.dump(customerData, f)


updateTravelBuddy()
#####----assumptions-----######
#delays with less than 20 minutes are considered
#final destination under 0.001 degrees are considered
#final time under 20 minutes on either side are considered
