from secrets import token_hex 
import time

import hashlib
import hmac
import base64

CONSUMER_SECRET   = "24102f8f97973af15600be3935f5f4cf927dee3907c406a2ae2506e97d756fba" #"87a296e9fdacb56b9bbc8b4afae54c01f8c5c0220341dbc6d06d67308d13106f" # (CLIENT SECRET)
TOKEN_SECRET      = "3ace7447837db695e3b39827d55d6c790692eb71dd2b3a3f4efd5f78ab330f01" #"eb3f07e309752951b49cfdf96667d9caf7ab21509a89f999eb9703853a2085d8"

class Credentials():

   NETSUITE_URL      = "https://6197523-sb1.suitetalk.api.netsuite.com/services/NetSuitePort_2020_1" #"https://webservices.netsuite.com/services/NetSuitePort_2020_1"
   # para extraer el mapeo usar:  python -m zeep 'https://webservices.netsuite.com/wsdl/v2020_1_0/netsuite.wsdl' > wsdl.txt
   NETSUITE_WSDL     = "https://webservices.netsuite.com/wsdl/v2020_1_0/netsuite.wsdl" 

   def __init__(self):

        self.ACCOUNT_NUMBER    = "6197523_SB1"
        self.APPLICATION_ID    = "8441E1A1-542B-475A-8C9A-F45D5670BEC5" #"565EB933-B612-4277-A72B-5EFBD18DD936"
        self.NAME              = "Momi - Sandbox"
        self.CONSUMER_KEY      = "295b8a477c0caaa2ea940069c52c194cdd402b7bf8a449ff322e56e3a1e884f0" #f25b76eb5b1851c75ac39e692a685dbe7f60842e362c43e6c4e53c35635371cc" # (CLIENT ID)
        self.TOKEN_ID          = "4a78a69173c565fa61b77341478f8e07aef5ea9b9e28cc3c5b78528010300b0c" #"566941115f6634f3a8e7ac9c4d580cd80042f176c560c2ee66cfbca12611d926"

   def getSignature(self):
        return Signature(self)

class Signature():

    def __init__(self, cred:Credentials):   
        self.ALGORITHM         = 'hmac-'+ hashlib.sha256().name     
        self.NONCE             = str(token_hex(32)) #token_urlsafe(32)
        self.TIMESTAMP         = str(round(time.time()))
         

        # TokenPassportSignature (Step1)
        base = "&".join([
                            cred.ACCOUNT_NUMBER, 
                            cred.CONSUMER_KEY,
                            cred.TOKEN_ID,
                            self.NONCE,
                            self.TIMESTAMP
                        ]
                        )
        key = "&".join ([
                            CONSUMER_SECRET,
                            TOKEN_SECRET 
                        ])
        
        self.SIGNATURE =  make_digest(base, key)

def make_digest(message, key):
    
    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')
    
    digester = hmac.new(key, message, hashlib.sha256)
    #signature1 = digester.hexdigest()
    signature1 = digester.digest()
    #print(signature1)
    
    #signature2 = base64.urlsafe_b64encode(bytes(signature1, 'UTF-8'))
    signature2 = base64.b64encode(signature1)    
    #print(signature2)

    resp = str(signature2, 'UTF-8')
    
    return resp 



if __name__ == "__main__":
    pass
    a = Credentials()
    print (a.getSignature().SIGNATURE)
