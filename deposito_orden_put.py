
#from os import stat_result
import netsuite as ns
from momi import regAbono

#from requests import Session 
#from html import unescape

from zeep import Client
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin

#from lxml import etree as ET
from datetime import datetime
from time import sleep

#from urllib.parse import urlparse

import requests as req


def subirAbono(registro, clienteNs=None):

  cabecera:regAbono = registro

  clienteNs = ns.NetSuiteClient(connect=True) if clienteNs==None else clienteNs 
  client = clienteNs.client
  
  with client.settings(raw_response=True):

    coreFactory  = client.type_factory('urn:core_2020_1.platform.webservices.netsuite.com')
    customerFactory  = client.type_factory('urn:customers_2020_1.transactions.webservices.netsuite.com')

    myRec = customerFactory.CustomerDeposit()
    myRec.externalId = '{0}-{1}'.format(cabecera.num_pedido, cabecera.num_abono) 
    myRec.salesOrder = coreFactory.RecordRef(internalId=cabecera.num_documento )
    myRec.tranDate = cabecera.fecha
    myRec.payment = cabecera.monto    
    #myRec.location = coreFactory.RecordRef(internalId=cabecera.ubicacion )
    #myRec.paymentMethod = coreFactory.RecordRef(internalId=cabecera.metodo_pago )

    resp = ns.upsertRecord(client, myRec, clienteNs.getTokenPass())
    
    return resp
      


if __name__ == '__main__':
   pass




