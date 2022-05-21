
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


def subirVentaCredito(master,  clienteNs=None):

  cabecera:regCabecera = master 

  clienteNs = ns.NetSuiteClient(connect=True) if clienteNs==None else clienteNs 
  client = clienteNs.client
  
  with client.settings(raw_response=False):

    salesFactory = client.type_factory('urn:sales_2020_1.transactions.webservices.netsuite.com')
    coreFactory = client.type_factory('urn:core_2020_1.platform.webservices.netsuite.com')
    msgFactory = client.type_factory('urn:messages_2020_1.platform.webservices.netsuite.com')
    customFactory = client.type_factory('urn:customization_2020_1.setup.webservices.netsuite.com')

    # cabecera
    myInvoice = salesFactory.Invoice()
    myNulo = coreFactory.NullField()

    # se inicializa el registro a partir de la orden
    myRef = coreFactory.InitializeRef()
    myRef.internalId = cabecera.id_orden
    myRef.type = 'salesOrder'

    myRec = coreFactory.InitializeRecord()
    myRec.type = 'invoice'
    myRec.reference = myRef

    resp = client.service.initialize(myRec, _soapheaders=clienteNs.getTokenPass())
    
    body = resp.body.readResponse
    if body.status.isSuccess:
        myInvoice = body.record    
        # solo se añade la informacion minima del pos
        myInvoice.externalId = cabecera.num_factura
        myInvoice.tranId = cabecera.cod_fiscal 
        myInvoice.paymentOption = coreFactory.RecordRef(internalId=cabecera.metodo_pago1 )
        
        #agregamos customs obligatorios
        myInvoice.customFieldList.customField.append(coreFactory.SelectCustomFieldRef(scriptId='custbody_ad_pa_tax_document_type', value=coreFactory.ListOrRecordRef(internalId=cabecera.formulario))) #se le añaden campos tipo custom


        # NOTA: se agregan preferencias al header para evitar errores con los campos readonly que vinieron de la inicializacion
        preferences = {'preferences' : msgFactory.Preferences(ignoreReadOnlyFields=True)}

        ns.grabarEntradaXML(client, 'upsert', myInvoice,  clienteNs.getTokenPass() | preferences)
        resp = ns.upsertRecord(client, myInvoice, clienteNs.getTokenPass() | preferences)
    
    return resp
      


if __name__ == '__main__':
  pass




