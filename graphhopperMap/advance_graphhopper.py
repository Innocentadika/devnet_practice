import requests
import urllib.parse

'''
Refer everything from onedrive folder devNet pdf 4.9.2 Lab
https://docs.graphhopper.com/
geo_url - the Geocoding URL to request longitude and latitude information for a location
 route_url - the Routing URL to request routing information from the point of origin to the destination
 loc1 - the parameter to specify the point of origin
 loc2 - the parameter to specify the destination
 key - the Graphhopper API key you retrieved from the Graphhopper website 
'''
route_url = "https://graphhopper.com/api/1/route?"
# loc1 = "Washington, D.C."
# loc2 = "Baltimore, Maryland"
key = "a0552be1-e9b3-4cc8-b74a-9b4757a7e958" # Replace with your Graphhopper API key 

def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ") 
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit":"1", "key":key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    # print(json_data)
    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat = (json_data["hits"][0]["point"]["lat"])
        lng = (json_data["hits"][0]["point"]["lng"])
        name = (json_data["hits"][0]["name"])
        value = (json_data["hits"][0]["osm_value"])
        
        if "country" in json_data["hits"][0]:
            country = (json_data["hits"][0]["country"])
        else:
            country=""
        
        if "state" in json_data["hits"][0]["state"]:
            state = (json_data["hits"][0]["state"])
        else:
            state=""
        
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
            
        elif len(state) !=0:
            new_loc = name + ", " + country
            
        else:
            new_loc = name
            
        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url) 
             
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status !=200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])
        
        
    return json_status,lat,lng,new_loc

while True:
    loc1 = input("Starting Location: ") 
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    
    loc2 = input("Destination: ") 
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 or dest[0] == 200:
        op="&point"+str(orig[1])+"%2C"+str(orig[2])
        dp="&point"+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key}) + op + dp
        paths_status = requests.get(paths_url).status_codes
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)

        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3])
        print("=================================================")

        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"])/1000/1.6
            km = (paths_data["paths"][0]["distance"])/1000
            sec = int(paths_data["paths"][0]["time"])/1000%60
            min = int(paths_data["paths"][0]["time"])/1000/60%60
            hr = int(paths_data["paths"][0]["time"])/1000/60/60
            print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
            print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec)) 
            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["time"]
                distance  = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance/1000, distance/1000/1.61))
                print("=============================================")
                
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************") 
                
                
        while True:
            print("\n+++++++++++++++++++++++++++++++++++++++++++++")
            print("Vehicle profiles available on Graphhopper:")
            print("+++++++++++++++++++++++++++++++++++++++++++++")
            print("car, bike, foot")
            print("+++++++++++++++++++++++++++++++++++++++++++++")
            
            profile=["car", "bike", "foot"]
            vehicle = input("Enter a vehicle profile from the list above: ") 
            
            if vehicle == "quit" or vehicle == "q":
                break
            elif vehicle in profile:
                vehicle = vehicle
                
            else:
                vehicle = "car"
                print("No valid vehicle profile was entered. Using the car profile.")  
                