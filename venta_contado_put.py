
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


def subirVentaContado(master, detail, clienteNs=None):

  cabecera:regCabecera = master 

  clienteNs = ns.NetSuiteClient(connect=True) if clienteNs==None else clienteNs 
  client = clienteNs.client
  
  with client.settings(raw_response=True):

    salesFactory = client.type_factory('urn:sales_2020_1.transactions.webservices.netsuite.com')
    coreFactory = client.type_factory('urn:core_2020_1.platform.webservices.netsuite.com')

    # cabecera
    myCashSale = salesFactory.CashSale()
    #myCashSale.source = cabecera.cod_fiscal  
    myCashSale.externalId = cabecera.num_factura #cuando se deja en blanco netsuite mnda el error: EXTERNALID_REQD: Esta operación requiere un valor para externalId 
    #myCashSale.tranId = cabecera.num_factura
    myCashSale.tranId = cabecera.cod_fiscal
    #myCashSale.salesEffectiveDate = cabecera.fecha_efectiva
    myCashSale.status = cabecera.estatus
    myCashSale.location = coreFactory.RecordRef(internalId=cabecera.cod_ubicacion ) #, type='location')
    myCashSale.tranDate = cabecera.fecha_transacc
    myCashSale.entity = coreFactory.RecordRef(internalId=cabecera.cod_cliente ) #, type='customer' )
    myCashSale.account = coreFactory.RecordRef(internalId=cabecera.num_cuenta, type='account')
    #myCashSale.salesRep = coreFactory.RecordRef(internalId=cabecera.cod_vendedor ) #, type='employee' ) #solo funciona si no esta activa la opcion de teams
    team = salesFactory.CashSaleSalesTeam( employee=coreFactory.RecordRef(internalId=cabecera.cod_vendedor ))
    teamList = salesFactory.CashSaleSalesTeamList()
    teamList.salesTeam.append(team)
    myCashSale.salesTeamList = teamList
    #myCashSale.paymentMethod = coreFactory.RecordRef(internalId=cabecera.metodo_pago )
    myCashSale.paymentOption = coreFactory.RecordRef(internalId=cabecera.metodo_pago1 )
    

    customFildList = coreFactory.CustomFieldList() #REM: los custom fields pueden ser de varios tipos ( String, Select, MultiSelect, Boolean, etc.) y deben tener un value diferente de None
    customFildList.customField.append(coreFactory.DoubleCustomFieldRef(scriptId='custbody_ad_dm_payment_amount_1', value=cabecera.monto_pago1 or 0 ))
    customFildList.customField.append(coreFactory.StringCustomFieldRef(scriptId='custbody_ad_dm_invoice_number', value=cabecera.num_factura ))
    if cabecera.metodo_pago2 != None:
       customFildList.customField.append(coreFactory.SelectCustomFieldRef(scriptId='custbody_ad_dm_payment_2', value=coreFactory.ListOrRecordRef(internalId=cabecera.metodo_pago2)) )
       customFildList.customField.append(coreFactory.DoubleCustomFieldRef(scriptId='custbody_ad_dm_amount_2', value=cabecera.monto_pago2 or 0))
    myCashSale.customFieldList = customFildList

    # items
    myCashSale.itemList = salesFactory.CashSaleItemList()
    for x in detail:
        y:regDetalle = x
        item = salesFactory.CashSaleItem(
                quantity = y.cantidad
              , item = coreFactory.RecordRef(internalId=y.cod_articulo) #, type='inventoryItem')
              , description = y.descripcion
              , line = y.linea
              , location = coreFactory.RecordRef(internalId=cabecera.cod_ubicacion if y.location == None else y.location ) #, type='location')
              , price = coreFactory.RecordRef(internalId=-1 , type='priceLevel')
              , rate = y.precio
                          
            
        )

        myCashSale.itemList.item.append(item)

    #ns.grabarEntradaXML(client, 'upsert', myCashSale, clienteNs.getTokenPass())
    resp = ns.upsertRecord(client, myCashSale, clienteNs.getTokenPass())
    
    return resp
      


if __name__ == '__main__':
   pass




