import json
import yaml

with open ('myfile.json','r') as json_file:
    ourjson = json.load(json_file)
    
print(ourjson, "\n")
print("The access token is: {}".format(ourjson['access_token']), "\n")
print("The access token expires in: {} seconds.".format(ourjson['expires_in']), "\n")
print("\n---")
print(yaml.dump(ourjson))


