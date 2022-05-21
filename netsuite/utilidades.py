from logging import exception
from lxml import etree as ET
from datetime import datetime
import xml.etree.ElementTree as xml
from io import BytesIO 
import requests as req
from time import sleep 
import ntplib

def convertXML(element):
    tree=xml.ElementTree(element)
    f = BytesIO() #archivo ficticio
    tree.write(f, encoding='utf-8', xml_declaration=True) 
    return f.getvalue() 


def grabarSalidaXML( nombre, dato):
    node = ET.fromstring(dato)
    tree = ET.ElementTree(node)
    tree.write(nombre+'_salida.txt', pretty_print=True)


def grabarEntradaXML(client, function, record, token):
    
    try:
      if record == None:
         node = client.create_message(client.service, function,  _soapheaders=token)
      else:
         node = client.create_message(client.service, function, record, _soapheaders=token)
      tree = ET.ElementTree(node)
      tree.write(function+'_entrada.xml', pretty_print=True)
    except Exception as e:
      raise  ValueError('Error al grabarEntradaXML',e.args[0])

def internetOK(intentos=0):

  cont = intentos - 1
  
  while cont < intentos:
    cont = cont + 1 if intentos > 0 else 0 
    timeout = 5
    try:
      request = req.get('http://www.netsuite.com', timeout=timeout)
      print("Connected to the Internet")
      break
    except (req.ConnectionError, req.Timeout) as exception:
      print("No internet connection.")  
      sleep (5)
    
    return  


def buscarHoraWeb():

  try:
      client = ntplib.NTPClient()
      response = client.request('pool.ntp.org')
      return response.tx_time
      #os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
  except:
      print('Could not sync with time server.')
      raise

  