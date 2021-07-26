from datetime import datetime
import netsuite as ns
from momi import DataBaseClient 
import logging
from momi import utility as util

import os

def nz(objeto, variables, default=None):
  resp = default
  try:
    for v in variables:
      resp = objeto[v] 
      if isinstance(resp, list): #el objeto es una lista?
        if len(resp)>0:
          resp = resp[0] #forzar primera incidencia
        else:
          return default
      objeto = resp 
  except:
    return default
  
  return resp 

def getCustomField(object, name, field):
  try:
    for c in object.customFieldList.customField:
      if c.scriptId == name:
        return nz(c,field)
    return
  except:
    return None


def getArgsFromRow(rec):
   precio_alt1 = 0
   precio_alt2 = 0
   precio_alt3 = 0
   precio_alt4 = 0

   for prec in rec.basic.otherPrices:
      precio_alt1 = prec.searchValue if prec.customLabel == 'Precio alternativo 1' else precio_alt1
      precio_alt2 = prec.searchValue if prec.customLabel == 'Precio alternativo 2' else precio_alt2
      precio_alt3 = prec.searchValue if prec.customLabel == 'Precio alternativo 3' else precio_alt3
      precio_alt4 = prec.searchValue if prec.customLabel == 'Precio en línea' else precio_alt4

   arr = (
      rec.basic.internalId[0].searchValue.internalId if rec.basic.internalId else None #internalId
    , rec.basic.itemId[0].searchValue if rec.basic.itemId else None #nombre
    , rec.basic.type[0].searchValue if rec.basic.type else None #tipo
    , rec.basic.quantityOnHand[0].searchValue if rec.basic.quantityOnHand else  None  #cantidad
    , rec.basic.stockUnit[0].searchValue.internalId if rec.basic.stockUnit else None #unidad
    , rec.inventoryLocationJoin.internalId[0].searchValue.internalId if rec.inventoryLocationJoin else None #location 
    , rec.basic.basePrice[0].searchValue if rec.basic.basePrice else None #precio
    , rec.basic.created[0].searchValue if rec.basic.created else None   #fec_creac
    , rec.basic.modified[0].searchValue if rec.basic.modified else None #fec_modif
    , None #lote
    , None #fecha_caduc ?
    , rec.basic.isInactive[0].searchValue if rec.basic.isInactive else None #inactivo
    , getCustomField(rec.basic,'custitem_ad_item_pos',['searchValue']) #codigo en el pos
    , getCustomField(rec.basic,'custitem_ad_item_group_pos',['searchValue','internalId'])
    , getCustomField(rec.basic,'custitem_ad_item_supply_group',['searchValue','internalId'])
    , rec.basic.upcCode[0].searchValue if rec.basic.upcCode else None #codigo de barra
    , getCustomField(rec.basic, 'custitem_ad_item_internal_upccode',['searchValue'])  #tipo interno (true) o externo (false)
    , rec.basic.taxSchedule[0].searchValue.internalId if rec.basic.taxSchedule else None #lleva impuesto 
    , precio_alt1 #precio alternativo 1
    , precio_alt2 #precio alternativo 2
    , precio_alt3 #precio alternativo 3
    , precio_alt4 #precio alternativo 4
    )

   return arr




def main(socket=None):


  # create logger
  #logger = logging.getLogger('__name__')

  # set up logging to file - see previous section for more details
  modulo = os.path.splitext(os.path.basename(__file__))[0]
  logging.basicConfig(level=logging.INFO,
                      #format='%(asctime)s %(name)-12s %(message)s',
                      #datefmt='%m-%d %H:%M',
                      format='%(asctime)s %(name)s - %(levelname)s - %(message)s', 
                      datefmt='%Y-%m-%d %I:%M:%S %p',
                      filename='./logs/' + modulo + '.log',
                      filemode='w')
  # define a Handler which writes INFO messages or higher to the sys.stderr
  console = logging.StreamHandler()
  #console.setLevel(logging.INFO)
  # set a format which is simpler for console use
  formatter = logging.Formatter('%(asctime)s: %(message)s')
  # tell the handler to use this format
  console.setFormatter(formatter)
  # add the handler to the root logger
  logging.getLogger('').addHandler(console)


  logger = logging.getLogger(__name__)
  

  logger.info('--- CARGA DE ARTICULOS DE NETSUITE ---')

  logger.info('Crendo cliente de Netsuite')
  clienteNs = ns.NetSuiteClient(connect=True)  

  util.transmitir(socket, 'mensajes', 'Conexión a Netsuite... OK')

  logger.info('Crendo cliente para MySQL')
  clienteMomi = DataBaseClient(connect=True) # al crearlo ya hay un cursor activo

  util.transmitir(socket, 'mensajes', 'Conexión a MySQL... OK')

  clienteMomi.connection.autocommit = True #queremos que insert cada sentencia ejecutada

  buscId =  'customsearch_ad_items_pos' # InternalId 418

  #buscId = ns.getSavedSearch(clienteNs, 'customsearch_ad_items_pos')
   
  logger.info('conectandose a netsuite - consulta %s' % buscId)
  searchResult = ns.itemCustomSearch(clienteNs, buscId, 100)

  if searchResult.status.isSuccess and searchResult.totalRecords > 0:
  
      util.transmitir(socket, 'mensajes', 'Cargando los datos...')

      sId = searchResult.searchId
      pagina_actual = 1
      paginas = searchResult.totalPages
      registros = searchResult.totalRecords
      logger.info('La cabecera indica %s registros extraídos' % registros)
  
      query =  """
                  insert into ns_items (
                    internalId 
                    , nombre     
                    , tipo       
                    , cantidad   
                    , unidad     
                    , ubicacion  
                    , precio     
                    , fec_creac  
                    , fec_modif  
                    , lote       
                    , fec_caduc  
                    , inactivo
                    , item_pos
                    , item_pos_group
                    , item_pos_supply
                    , codigo_barra
                    , tipo_codigo_barra
                    , codigo_impuesto
                    , precio_alt1
                    , precio_alt2
                    , precio_alt3
                    , precio_alt4

                  ) 
                  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
      cont = 0

      logger.info('Inicia el ciclo de carga con el contador en %s' % cont  )

      #REGISTRAR DATOS ANTERIORES ANTES DE TRUNCAR
      clienteMomi.cursor.callproc('pa_registrar_items', args=('ant',)) #la coma es para forzar la creación de una tupla o sequencia

      logger.info('Truncando la tabla de items en MySQL')
      clienteMomi.cursor.execute ('truncate table ns_items')

      logger.info('Iniciando ciclo de carga en MySQL')

      # Procesando los resultados
      while pagina_actual <= paginas:

          for rec in searchResult.searchRowList.searchRow:
              cont+=1
              args = getArgsFromRow(rec)

              logger.info('se cargo el item %s - %s' % (args[0], args[1]))
              clienteMomi.cursor.execute (query, args)
              #clienteMomi.connection.commit ()
              if cont % 20 == 0:
                util.transmitir(socket, 'procesando', {'cantidad' : cont} )
             
          pagina_actual += 1
          searchResult = ns.SearchMore(clienteNs, sId, pagina_actual)

      #procesando el resto de las paginas 
      # while pagina_actual < paginas:
      #   pagina_actual += 1
      #   searchResult = ns.SearchMore(clienteNs, sId, pagina_actual)
      #   if searchResult.status.isSuccess:  
      #     for rec in searchResult.searchRowList.searchRow:
      #         cont+=1
      #         args = getArgsFromRow(rec)
      #         logger.info('se cargo el item %s - %s' % (args[0], args[1]))
      #         clienteMomi.cursor.execute (query, args)

      #         if cont % 20 == 0:
      #            util.transmitir(socket, 'procesando', {'cantidad' : cont} )

      #REGISTRAR DATOS RECIEN CARGADOS
      clienteMomi.cursor.callproc('pa_registrar_items', args= ('act',))

      logger.info('Termina el ciclo de carga con el contador en %s ' % cont )

      

#----------------

if __name__ == "__main__":
  main() 