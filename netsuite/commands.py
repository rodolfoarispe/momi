import xml.etree.ElementTree as ET
from xml.etree import cElementTree as cET # mas rapido?? hay que probar 

from zeep import client as cli
from html import unescape

#from netsuite.credenciales import Credentials  #SOLO PARA HINT

def searchAccount(client, cuenta, token):

    mySearchStrType = client.get_type('{urn:core_2020_1.platform.webservices.netsuite.com}SearchStringField')   
    mySearchStr = mySearchStrType(
                    operator = 'is'
                    , searchValue = cuenta
                )
    myAccountSearchBasicType = client.get_type('{urn:common_2020_1.platform.webservices.netsuite.com}AccountSearchBasic')
    myAccountSearchBasic = myAccountSearchBasicType(number=mySearchStr)
    
    try:
        response = client.service.search(myAccountSearchBasic, _soapheaders=token)
    except:
        raise 

    accId = ''      
    if response.reason=='OK':
      data = ET.fromstring(response.content)
      accId = data.find('.//{urn:core_2020_1.platform.webservices.netsuite.com}record').get('internalId')

    return accId 


def upsertRecord(client, registro, token ):

    with client.settings(raw_response=True):

        try:
            response = client.service.upsert(record=registro, _soapheaders=token)
        except:
            raise 

        body     = ET.fromstring(response.content)[1] 
        status   = body.find('.//{urn:messages_2020_1.platform.webservices.netsuite.com}writeResponse')[0]
        baseRef  = body.find('.//{urn:messages_2020_1.platform.webservices.netsuite.com}writeResponse')[1]
        internal = baseRef.get('internalId')

        estatusIsSuccess = status.get('isSuccess')

        mensajes = []
        for detail in status:      
            statusDetailType = detail.get('type') 
            statusDetailCode = detail[0].text if statusDetailType != None else None
            statusDetailMessage = unescape(detail[1].text) if statusDetailType != None else None
            mensajes.append({'isSuccess':estatusIsSuccess, 'tipo':statusDetailType, 'codigo':statusDetailCode, 'mensaje': statusDetailMessage}) 

    return {'isSuccess':estatusIsSuccess, 'mensajes':mensajes, 'internalId':internal} 


def initializeRecord(client, registro, token ):

    try:
        response = client.service.initialize(record=registro, _soapheaders=token)
    except:
        raise 

    body     = ET.fromstring(response.content)[1] 
    status   = body.find('.//{urn:messages_2020_1.platform.webservices.netsuite.com}writeResponse')[0]
    baseRef  = body.find('.//{urn:messages_2020_1.platform.webservices.netsuite.com}writeResponse')[1]
    internal = baseRef.get('internalId')

    estatusIsSuccess = status.get('isSuccess')

    mensajes = []
    for detail in status:      
        statusDetailType = detail.get('type') 
        statusDetailCode = detail[0].text if statusDetailType != None else None
        statusDetailMessage = unescape(detail[1].text) if statusDetailType != None else None
        mensajes.append({'isSuccess':estatusIsSuccess, 'tipo':statusDetailType, 'codigo':statusDetailCode, 'mensaje': statusDetailMessage}) 

    return {'isSuccess':estatusIsSuccess, 'mensajes':mensajes, 'internalId':internal} 


def itemSearch(clientNs):

    itemSearch = clientNs.searchFactory.ItemSearch()
    itemSearchBasic = clientNs.commonFactory.ItemSearchBasic(isInactive=False)    

    itemSearch.basic = itemSearchBasic
    
    searchBody = ET.parse(f'itemResponse.xml').getroot()[1] #body
    searchResult = clientNs.client.service.search(itemSearch, _soapheaders=clientNs.getTokenPass())
    
    searchResult = ET.parse(searchResult.content)

    resp = buscarDatoXML(searchBody, ['searchResult','status'], 'urn:core_2020_1.platform.webservices.netsuite.com')
    status = resp.get('isSuccess') if resp != None else None 

    resp = buscarDatoXML(searchBody, ['searchResult','totalRecords'], 'urn:core_2020_1.platform.webservices.netsuite.com')
    totalRecords = int(resp.text) if resp != None else 0

    searchId = buscarDatoXML(searchBody, ['searchResult','searchId'], 'urn:core_2020_1.platform.webservices.netsuite.com')
    pageSize = buscarDatoXML(searchBody, ['searchResult','pageSize'], 'urn:core_2020_1.platform.webservices.netsuite.com')
    totalPages = buscarDatoXML(searchBody, ['searchResult','totalPages'], 'urn:core_2020_1.platform.webservices.netsuite.com')

    if status=='true' and totalRecords>0:
        registros =  buscarDatoXML(searchBody, ['searchResult','recordList'], 'urn:core_2020_1.platform.webservices.netsuite.com')

        for reg in registros:
            dicc = {}
            dicc['type'] =  (reg.get('{http://www.w3.org/2001/XMLSchema-instance}type'))
            dicc['internalId'] = reg.get('internalId')
            dicc['lastModifiedDate'] = buscarDatoXML(reg, ['lastModifiedDate'], 'urn:accounting_2020_1.lists.webservices.netsuite.com' ).text
            print (dicc) 




def getSavedSearch(clienteNs, searchId):

    #buscamos el Id del serchRecord
    savedSearchRecord = clienteNs.coreFactory.GetSavedSearchRecord()

    #savedSearchRecord.searchTypeSpecified = True
    #savedSearchRecord.searchType = clienteNs.accountingFactory.ItemSearchAdvanced()
    
    resp = clienteNs.client.service.getSavedSearch(savedSearchRecord, _soapheaders=clienteNs.getTokenPass())

    return resp 

def  itemCustomSearch(clientNs, searchId, pageSize=500):

    #itemSearch = clientNs.searchFactory.ItemSearch()

    #definimos alias para los contructores
    tref = clientNs.coreFactory.RecordRef 
    tdate = clientNs.coreFactory.SearchColumnDateField
    tsel = clientNs.coreFactory.SearchColumnSelectField
    tbool = clientNs.coreFactory.SearchColumnBooleanField
    tstr = clientNs.coreFactory.SearchColumnStringField


    itemSearchRow = clientNs.accountingFactory.ItemSearchRow()
    itemSearchRow.basic = clientNs.commonFactory.ItemSearchRowBasic(
         internalId = tsel()
       , created = tdate()
       , itemId = tstr()
    )

    #customSearch = clientNs.accountingFactory.ItemSearchAdvanced(savedSearchId = searchId, columns=itemSearchRow)  
    customSearch = clientNs.accountingFactory.ItemSearchAdvanced(savedSearchScriptId = searchId)  #con internalid usar savedSearchId  

    #searchBody = ET.parse(f'itemResponse.xml').getroot()[1] #body
 
    resp = ""
    with clientNs.client.settings(raw_response=False):

      searchPref = {'searchPreferences' : clientNs.messageFactory.SearchPreferences(bodyFieldsOnly=False, pageSize=pageSize , returnSearchColumns=True )}
      
      resp = clientNs.client.service.search(customSearch, _soapheaders=clientNs.getTokenPass() | searchPref)
    

    searchResult = resp.body.searchResult

    return searchResult 

def SearchMore(clientNs, searchId, page):
    searchResult = None
    
    with clientNs.client.settings(raw_response=False):
      #searchPref = clientNs.messageFactory.SearchPreferences(bodyFieldsOnly=False, pageSize=1000 , returnSearchColumns=False )
      #clientNs.client.service.search.preferences = searchPref
      resp = clientNs.client.service.searchMoreWithId(searchId, page, _soapheaders=clientNs.getTokenPass())
      searchResult = resp.body.searchResult

    return searchResult 

def  Search(clientNs, searchRecordType, pageSize=500):
 
    resp = ""
    with clientNs.client.settings(raw_response=False):
      searchPref = { 'searchPreferences': clientNs.messageFactory.SearchPreferences(bodyFieldsOnly=False, pageSize=pageSize , returnSearchColumns=True ) }
      
      resp = clientNs.client.service.search(searchRecordType, _soapheaders=clientNs.getTokenPass() | searchPref)

    searchResult = resp.body.searchResult

    return searchResult 



class UpsertHeader():
    # Preparamos la cabecera
    def __init__(self):
        self.root = ET.Element('soap:Body')
        self.function = ET.SubElement(self.root,'upsert')
        self.function.set('xmlns','urn:messages_2020_2.platform.webservices.netsuite.com')



### TOMADO DE: https://code.activestate.com/recipes/410469-xml-as-dictionary/

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''

    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


## devuelve un elemento XML a partir a partir de un Element y arreglo jerarquico del datos buscados
def buscarDatoXML (p_elemento, p_dato, namespace) -> ET.Element :
    resp = None
    try :
        for dato in p_dato:
           d = './/ns:'+ dato
           resp = p_elemento.find(d, dict(ns=namespace) )
           p_elemento = resp #buscar 
           if resp==None:
              exit
    except:
       resp = None
    return resp