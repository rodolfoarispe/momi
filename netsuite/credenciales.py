from secrets import token_hex 
import time

import hashlib
import hmac
import base64

CONSUMER_SECRET   = "87a296e9fdacb56b9bbc8b4afae54c01f8c5c0220341dbc6d06d67308d13106f" # (CLIENT SECRET)
TOKEN_SECRET      = "1f49b8af9c051c8ca02f2c98afa5d2db8ad561e4d231d5f0b626272d6669351a" #"eb3f07e309752951b49cfdf96667d9caf7ab21509a89f999eb9703853a2085d8"

class Credentials():

   NETSUITE_URL      = "https://webservices.netsuite.com/services/NetSuitePort_2020_1"
   # para extraer el mapeo usar:  python -m zeep 'https://webservices.netsuite.com/wsdl/v2020_1_0/netsuite.wsdl' > wsdl.txt
   NETSUITE_WSDL     = "https://webservices.netsuite.com/wsdl/v2020_1_0/netsuite.wsdl" 

   def __init__(self):

        self.ACCOUNT_NUMBER    = "6197523_SB1"
        self.APPLICATION_ID    = "3CEE6B13-4B5E-4E42-9B61-EE78889973DB"
        self.NAME              = "Momi - Sandbox"
        self.CONSUMER_KEY      = "f25b76eb5b1851c75ac39e692a685dbe7f60842e362c43e6c4e53c35635371cc" # (CLIENT ID)
        self.TOKEN_ID          =   "135a8997d02ff3bfc6daf555587b1fd4f3dd95a31e3642c3d43460d43c9f2ca6" #"566941115f6634f3a8e7ac9c4d580cd80042f176c560c2ee66cfbca12611d926"

   def getSignature(self):
        return Signature(self)

class Signature():

    def __init__(self, cred:Credentials):   
        self.ALGORITHM         = 'hmac-'+ hashlib.sha1().name     
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
    
    digester = hmac.new(key, message, hashlib.sha1)
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
