
#from os import stat_result
from netsuite.commands import upsertRecord
from netsuite.client import NetSuiteClient
import netsuite as ns
from momi import regCabecera, regDetalle

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


def subirPago(master, clienteNs=None):

  cabecera:regCabecera = master 

  clienteNs = ns.NetSuiteClient(connect=True) if clienteNs==None else clienteNs 
  client = clienteNs.client
  
  with client.settings(raw_response=True):

    customerFactory = client.type_factory('urn:customers_2020_1.transactions.webservices.netsuite.com')
    coreFactory = client.type_factory('urn:core_2020_1.platform.webservices.netsuite.com')

    # cabecera
    myCustomerDeposit = customerFactory.CustomerDeposit()
    #obligatorios
    myCustomerDeposit.payment = cabecera.monto_pago1
    myCustomerDeposit.transDate = cabecera.fecha_transacc
    myCustomerDeposit.externalId = cabecera.num_factura
    myCustomerDeposit.customer = coreFactory.RecordRef(internalId=cabecera.cod_cliente )

    #opcionales
    myCustomerDeposit.undepFunds = cabecera.estatus
    #myCustomerDeposit.account 
    #yCustomerDeposit.salesOrder
    #myCustomerDeposit.status
    myCustomerDeposit.paymentOption = coreFactory.RecordRef(internalId=cabecera.metodo_pago1 )
    #myCustomerDeposit.undepFunds = True
  
    resp = ns.upsertRecord(client, myCustomerDeposit, clienteNs.getTokenPass())
    
    return resp
      

if __name__ == '__main__':
   pass




