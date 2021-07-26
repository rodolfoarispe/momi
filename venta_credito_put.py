
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


def subirVentaCredito(master, detail, clienteNs=None):

  cabecera:regCabecera = master 

  clienteNs = ns.NetSuiteClient(connect=True) if clienteNs==None else clienteNs 
  client = clienteNs.client
  
  with client.settings(raw_response=True):

    salesFactory = client.type_factory('urn:sales_2020_1.transactions.webservices.netsuite.com')
    coreFactory = client.type_factory('urn:core_2020_1.platform.webservices.netsuite.com')

    # cabecera
    myInvoice = salesFactory.Invoice()
    myInvoice.source = cabecera.cod_fiscal 
    #myInvoice.salesRep = coreFactory.RecordRef(internalId=cabecera.cod_vendedor , type='employee' )
    myInvoice.externalId = cabecera.num_factura
    myInvoice.status = cabecera.estatus
    myInvoice.location = coreFactory.RecordRef(internalId=cabecera.cod_ubicacion, type='location')
    myInvoice.tranDate = cabecera.fecha_transacc
    myInvoice.entity = coreFactory.RecordRef(internalId=cabecera.cod_cliente , type='customer' )
    #myInvoice.account = coreFactory.RecordRef(internalId=cabecera.num_cuenta, type='account') #Account Receivable

    # detalle
    for x in detail:
        y:regDetalle = x

        item = salesFactory.InvoiceItem(
                quantity = y.cantidad
              , item = coreFactory.RecordRef(internalId=y.cod_articulo, type='inventoryItem')
              , description = y.descripcion
              , line = y.linea
              , rate = y.precio
              
            
        )

        myInvoice.itemList = salesFactory.InvoiceItemList()
        myInvoice.itemList.item.append(item)

    resp = ns.upsertRecord(client, myInvoice, clienteNs.getTokenPass())
    
    return resp
      


if __name__ == '__main__':
  pass




