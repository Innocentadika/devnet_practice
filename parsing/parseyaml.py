import json
import yaml

with open('myfile.yaml','r') as safe_file:
    ouryaml = yaml.safe_load(safe_file)
    
# print(ouryaml)
print("The access token is: {}".format(ouryaml['access_token']), "\n")
print("The access token expires in: {} seconds.".format(ouryaml['expires_in']))
print("\n\n")
print(json.dumps(ouryaml, indent=4))