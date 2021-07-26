# PROGRAMA DE EJEMPLO
# muestra como armar la cabecera xml para un registro tipo Customer

import os
import mysql.connector
from mysql.connector import errorcode

#import xml.etree.ElementTree as xml
import xml.etree.ElementTree as ET
import netsuite as ns

# Get environment variables
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')
usr = os.getenv('DB_USER')
pwd = os.getenv('DB_PASSWORD') 

DB_HOST     = 'localhost' if host == None else host 
DB_NAME     = 'datapos'   if db == None else db
DB_USER     = 'usuario2'  if usr == None else usr 
DB_PASSWORD = '123456789' if pwd == None else pwd 



def GenerateXML(fileName):

    config = {
      'user': DB_USER,
      'password': DB_PASSWORD,
      'host': DB_HOST,
      'database': DB_NAME,
      'raise_on_warnings': True
    }

    try:
      cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
      cnx.close()

    comando = ns.UpsertHeader()

    ns.CustomerHeader(comando.function,
                 ID="14", 
                 COMPANY="ZETEKI TECHNOLOGIES", 
                 EMAIL="rodolfoarispe@zeteki.net")
  
    tree=ET.ElementTree(comando.root)
    with open(fileName,'wb') as file:
      tree.write(file, encoding='utf-8', xml_declaration=True)  

if __name__ == "__main__":
  salida = 'customers.xml'
  GenerateXML(salida)
  print ("Archivo %s generado exitosamente" % salida )