
from logging import exception, raiseExceptions
from requests.adapters import HTTPResponse
from netsuite.credenciales import Credentials ##SOLO USAR COMO HINT

from urllib.parse import urlparse

from zeep import Client, Settings
import zeep.exceptions as zerr
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin

class NetSuiteClient():

    def __init__(self, connect=False, cred:Credentials=None):

      self.credenciales = Credentials() if cred == None else cred 
      self.client = None

      if connect == True:
        self.Connect()



    def Connect(self):
      wsdl = self.credenciales.NETSUITE_WSDL
      transport = Transport(operation_timeout=120)
      #settings = Settings(strict=False, xml_huge_tree=True)
      settings = Settings(strict=True, xsd_ignore_sequence_order=True,  xml_huge_tree=True)

      try:
          # SE CREA EL CLIENTE
          self.client = Client(wsdl=wsdl, transport=transport, settings=settings)

          #SE CREAN LAS FABRICAS DE TIPOS COMUNES
          self.accountingFactory = self.client.type_factory('urn:accounting_2020_1.lists.webservices.netsuite.com')
          self.commonFactory = self.client.type_factory('urn:common_2020_1.platform.webservices.netsuite.com')
          self.coreFactory = self.client.type_factory('urn:core_2020_1.platform.webservices.netsuite.com')
          self.messageFactory = self.client.type_factory('urn:messages_2020_1.platform.webservices.netsuite.com')
          self.typeSalesFactory = self.client.type_factory('urn:types.sales_2020_1.transactions.webservices.netsuite.com')
          self.coreTypesFactory = self.client.type_factory('urn:types.core_2020_1.platform.webservices.netsuite.com')
          self.salesFactory = self.client.type_factory('urn:sales_2020_1.transactions.webservices.netsuite.com')

          url = self.client.service.getDataCenterUrls(self.credenciales.ACCOUNT_NUMBER)

      except:
          raise 

      urlRespType = self.client.get_type('ns0:GetDataCenterUrlsResult')
      urlResp = urlRespType(
            status=url.body.getDataCenterUrlsResult.status,
            dataCenterUrls = url.body.getDataCenterUrlsResult.dataCenterUrls
        )

      #self.domain_url = url['body']['getDataCenterUrlsResult']['dataCenterUrls']['webservicesDomain'] + pathAndQuery
      originalUri = urlparse (self.credenciales.NETSUITE_URL) # uri para servicios generico
      pathAndQuery = originalUri.path + originalUri.query
      self.domain_url = urlResp.dataCenterUrls.webservicesDomain + pathAndQuery

      self.client.service._binding_options["address"] = self.domain_url
      

    def getTokenPass(self):

        sign = self.credenciales.getSignature() 

        tokenSignatureType = self.client.get_type('ns0:TokenPassportSignature')
        tokenSignature = tokenSignatureType()
        tokenSignature['algorithm'] =   sign.ALGORITHM
        tokenSignature['_value_1']  =   sign.SIGNATURE
        
        tokenPassType = self.client.get_type('ns0:TokenPassport')
        tokenPass = tokenPassType(
              account       = self.credenciales.ACCOUNT_NUMBER
            , consumerKey   = self.credenciales.CONSUMER_KEY
            , token         = self.credenciales.TOKEN_ID
            , nonce         = sign.NONCE
            , timestamp     = sign.TIMESTAMP
            , signature     = tokenSignature
          
        )

        return {'tokenPassport':tokenPass}


