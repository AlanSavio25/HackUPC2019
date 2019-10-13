from flask import Flask
import json
from pprint import pprint
import requests
app = Flask(__name__)

API_Endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
key = "AIzaSyB9IXEkHM_WDXz59PaY_ncyyijaJXvi-XM"

@app.route('/addToDB', methods = ['POST'])
def addDailyReportToDB():
    data = request.get_json()
    print("You have received request.json")
    print(data)
    with open('customerData.json') as f:
        customerData = json.load(f)
    with open('dailyReport.json') as f:
        dailyData = json.load(f)
    customerData[dailyData["custID"]][dailyData["day"]].append(dailyData["trips"])
    pprint(customerData)
    with open('customerData.json', 'w') as f:
        json.dump(customerData, f)
        updateTravelBuddy()
        
@app.route('/travelPartner', methods = ['GET'])
def getTravelPartnerDetails():
    with open('travelBuddy.json') as e:
        print("HELLO WORLD")
        return json.load(e)

def timeDifference(origins_lat, origins_long, dest_lat, dest_long):
    url = API_Endpoint + str(origins_lat) + "," + str(origins_long) + "&destinations=" + str(dest_lat) + "," + str(dest_long) + "&mode=driving&key=" + key
    res = requests.post(url = url)
    jsondata = json.loads(res.text)
    # print(jsondata['rows'][0]['elements'][0]['duration']['text'])
    delay = jsondata['rows'][0]['elements'][0]['duration']['text']
    if len(delay.split(' '))==4:
        time = int(delay.split(' ')[0])*60 + int(delay.split(' ')[2])
    else:
        time =  int(delay.split(' ')[0])
    return time
# print(res.text.duration.text)

def close(driver, passenger):
    dist = (driver[0]-passenger[0])**2
    dist += (driver[1]-passenger[1])**2
    if (dist<0.01):
        return True
    else:
        return False

def matchingEndTime(driver,passenger):
    diff = abs(driver-passenger)
    if(diff<200):
        return True
    else:
        return False

def updateTravelBuddy():
    with open('customerData.json') as f:
        customerData = json.load(f)
	with open('profile.json') as f:
        customerProfile = json.load(f)

        with open('travelBuddy.json') as e:
            travelBuddy = json.load(e)
        for driver in customerData.keys():
            for day in customerData[driver].keys():
                for trip in customerData[driver][day]:
                    for passenger in customerData.keys():
                        for trip2 in customerData[passenger][day]:
                            if(close(trip["stopPlace"],trip2["stopPlace"]) and matchingEndTime (trip["stopTime"],trip2["stopTime"]) and (driver!=passenger)):
                            	delay = timeDifference(trip['startPlace'][0], trip['startPlace'][1], trip['stopPlace'][0], trip['stopPlace'][1])
                                #print("delay is: " + str(delay))
                               	if delay<=25:
									isFriends = ([driver,passenger] in customerProfile["friendlist"]) or ([passenger, driver] in customerProfile["friendlist"])
                                    travelBuddy[day].append({"driver":driver,"passenger":passenger, "destTime":int(trip["stopTime"]), "destLoc": trip["stopPlace"], "delay": delay, "passName": customerProfile[passenger], "isFriend": isFriends})

        with open('travelBuddy.json', 'w') as f:
            json.dump(travelBuddy, f)

#####----assumptions-----######
#delays with less than 20 minutes are considered
#final destination under 0.00001 degrees are considered
#final time under 20 minutes on either side are considered


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    updateTravelBuddy()
    app.debug = True
    app.run()
