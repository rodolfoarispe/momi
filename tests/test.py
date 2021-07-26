

from netsuite2 import client as nsclient
from netsuite2.api.customer import get_customer

conf = {}

NETSUITE_URL      = "https://webservices.netsuite.com/services/NetSuitePort_2020_1"
NETSUITE_WSDL     = "https://webservices.netsuite.com/wsdl/v2020_1_0/netsuite.wsdl" 

ACCOUNT_NUMBER    = "6197523_SB1"
APPLICATION_ID    = "3CEE6B13-4B5E-4E42-9B61-EE78889973DB"
NAME              = "Momi - Sandbox"
CONSUMER_KEY      = "f25b76eb5b1851c75ac39e692a685dbe7f60842e362c43e6c4e53c35635371cc" # (CLIENT ID)
TOKEN_ID          = "566941115f6634f3a8e7ac9c4d580cd80042f176c560c2ee66cfbca12611d926"



conf['wsdlUrl'] = NETSUITE_WSDL
conf['applicationId'] = APPLICATION_ID
conf['passportType'] = 'tba' #nlauth or tba    
conf['tokenPassport'] = {}    
conf['tokenPassport']['account'] = ACCOUNT_NUMBER    
conf['tokenPassport']['consumerKey'] = CONSUMER_KEY
conf['tokenPassport']['consumerSecret'] = CONSUMER_SECRET
conf['tokenPassport']['tokenId'] = TOKEN_ID
conf['tokenPassport']['tokenSecret'] = TOKEN_SECRET
conf['tokenPassport']['hashAlgorithm'] = None #usar default


conf = nsclient.parse_api_config(conf)

app = nsclient.NetsuiteApiClient(conf)

url = app.client.service.getDataCenterUrls(ACCOUNT_NUMBER)
wsd = url.body.getDataCenterUrlsResult.dataCenterUrls.webservicesDomain

# print names of first 100 customers
for internal_id in range(100):
    customer = get_customer(app, internal_id)
    if customer:
        print(customer.firstName, customer.lastName)

