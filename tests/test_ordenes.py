#-- agregando el directorio padre
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#----


import netsuite as ns


clienteNs = ns.NetSuiteClient(connect=True)  

buscId =  'customsearch_ad_dm_sales_order' 

SearchRecordType = clienteNs.salesFactory.TransactionSearchAdvanced(savedSearchScriptId = buscId)  

with clienteNs.client.settings(raw_response=True):
    searchPref = clienteNs.messageFactory.SearchPreferences(bodyFieldsOnly=False, pageSize=1000 , returnSearchColumns=True )
    clienteNs.client.service.search.preferences = searchPref
    resp = clienteNs.client.service.search(SearchRecordType, _soapheaders=clienteNs.getTokenPass())
    
    ns.grabarSalidaXML('orden_cabecera', resp._content)
    