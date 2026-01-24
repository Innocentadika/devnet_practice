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
        json_data = requests.get(url).json
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
        if status_code !=200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])
        new_loc=location
        
    return json_status,lat,lng,new_loc

while True:
    loc1 = input("Starting Location: ") 
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    print(orig)
    
    loc2 = input("Destination: ") 
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    print(dest) 
