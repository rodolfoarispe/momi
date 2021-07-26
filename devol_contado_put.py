
#from os import stat_result
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


def subirDevolucionContado(master, detail, clienteNs=None):

  cabecera:regCabecera = master 

  clienteNs = ns.NetSuiteClient() if clienteNs==None else clienteNs 
  client = clienteNs.client
  
  with client.settings(raw_response=True):

    customerTransFactory = client.type_factory('urn:customers_2020_1.transactions.webservices.netsuite.com')
    coreFactory = client.type_factory('urn:core_2020_1.platform.webservices.netsuite.com')

    # cabecera
    myCashRefund = customerTransFactory.CashRefund()
    myCashRefund.source = cabecera.cod_fiscal 
    myCashRefund.externalId = cabecera.num_factura
    #myCashRefund.tranId = cabecera.num_factura
    myCashRefund.status = cabecera.estatus
    myCashRefund.location = coreFactory.RecordRef(internalId=cabecera.cod_ubicacion ) #, type='location')
    myCashRefund.tranDate = cabecera.fecha_transacc
    myCashRefund.entity = coreFactory.RecordRef(internalId=cabecera.cod_cliente ) #, type='customer' )
    myCashRefund.account = coreFactory.RecordRef(internalId=cabecera.num_cuenta, type='account')
    myCashRefund.salesRep = coreFactory.RecordRef(internalId=cabecera.cod_vendedor ) #, type='employee' )
    myCashRefund.paymentMethod = coreFactory.RecordRef(internalId=cabecera.metodo_pago1 )
    myCashRefund.itemList = customerTransFactory.CashRefundItemList()

    # items
    for x in detail:
        y:regDetalle = x
        item = customerTransFactory.CashRefundItem(
                quantity = y.cantidad
              , item = coreFactory.RecordRef(internalId=y.cod_articulo) #, type='inventoryItem')
              , description = y.descripcion
              , line = y.linea
              , location = coreFactory.RecordRef(internalId=cabecera.cod_ubicacion if y.location == None else y.location ) #, type='location')
              , price = coreFactory.RecordRef(internalId=-1 , type='priceLevel')
              , rate = y.precio
                          
            
        )

        myCashRefund.itemList.item.append(item)

    resp = ns.upsertRecord(client, myCashRefund, clienteNs.getTokenPass())
    
    return resp
      


if __name__ == '__main__':
   pass




