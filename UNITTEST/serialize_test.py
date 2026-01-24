import dicttoxml    # serialization library
import requests     # http request library
auth = {            # Python dict, containing authentication info
  "user": {
    "username": "myemail@mydomain.com",
    "key": "90823ff08409408aebcf4320384"
  }
}
get_services_query = "https://myservice.com/status/services"
xmlstring = dicttoxml(auth)       # convert dict to XML in string form
myresponse = requests.get(get_services_query,auth=xmlstring)  # query service

# # extract XML information into a form that Python could access conveniently
# mport untangle     # xml parser library
# myreponse_python = untangle.parse(myresponse)
# print myreponse_python.services.service[1].name.cdata,myreponse_python.services.service[1].status.cdata