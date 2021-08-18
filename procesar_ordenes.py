import netsuite as ns
from momi import utility as util
from momi import DataBaseClient 
import logging

from datetime import datetime

import os

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



def main(socket=None):
  logger = logging.getLogger(__name__)
  

  logger.info('--- CARGA DE ARTICULOS DE NETSUITE ---')
  logger.info('Crendo cliente de Netsuite')
  clienteNs = ns.NetSuiteClient(connect=True)  
  util.transmitir(socket, 'orders.mensajes', 'Conexión a Netsuite... OK')

  logger.info('Crendo cliente para MySQL')
  clienteMomi = DataBaseClient(connect=True) 
  util.transmitir(socket, 'orders.mensajes', 'Conexión a MySQL... OK')

  clienteMomi.connection.autocommit = True #queremos que insert cada sentencia ejecutada      

  # CONTADORES
  cont_cabecera = 0
  cont_linea = 0


#------DETALLES--------------

  buscId =  'customsearch_ad_dm_sales_order_details_2' #InternalId 406 # 

  logger.info('conectandose a netsuite - consulta de detalles %s' % buscId)

  SearchRecordType = clienteNs.salesFactory.TransactionSearchAdvanced(savedSearchScriptId = buscId) #cuando es por id usar savedSearchId  
  
  searchResult = ns.Search(clienteNs, SearchRecordType)

  if searchResult.status.isSuccess and searchResult.totalRecords>0:  

      util.transmitir(socket, 'orders.mensajes', 'Cargando los datos...')

      sId = searchResult.searchId
      paginas = searchResult.totalPages
      registros = searchResult.totalRecords
      logger.info('El registro de control de netsuite indica %s registros' % registros)
  

      query =  """
         insert into ns_ordenes_detalle (
                  fecha                
                , cliente_internalId    
                , num_documento        
                , articulo_internalId   
                , articulo_descr       
                , cantidad             
                , precio       
                , importe_bruto        
                , nota                 
                , dedicatoria          
                , ubicacion            
                , impuesto
                , linea
            ) 
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """


      logger.info('Inicia el ciclo de carga de detalles, contador en %s' % cont_linea  )

      logger.info('Truncando la tabla de detalle en MySQL')
      clienteMomi.cursor.execute ('truncate table ns_ordenes_detalle')

      logger.info('Iniciando ciclo de carga en MySQL')
      for rec in searchResult.searchRowList.searchRow:
          cont_linea +=1
          args = (
               nz(rec.basic, ['tranDate','searchValue'])
             , nz(rec.basic, ['entity','searchValue', 'internalId'])
             , nz(rec.basic, ['tranId','searchValue'])
             , nz(rec.basic, ['item','searchValue', 'internalId']) 
             , nz(rec.itemJoin, ['itemId','searchValue']) #item descr
             , nz(rec.basic, ['quantity','searchValue'])
             , nz(rec.basic, ['rate','searchValue'])
             , nz(rec.basic, ['grossAmount','searchValue'])
             , nz(rec.basic, ['memo','searchValue'])
             , getCustomField(rec.basic, 'custcol_ad_dm_dedication', ['searchValue'])
             , nz(rec.basic, ['location','searchValue','internalId']) 
             , nz(rec.basic, ['taxAmount','searchValue'])
             , nz(rec.basic, ['lineSequenceNumber','searchValue'])

          )

          clienteMomi.cursor.execute (query, args)
          logger.info('se cargo el documento %s - item %s' % (args[2], args[3]))
          clienteMomi.connection.commit ()

          if cont_linea % 10 == 0:
             util.transmitir(socket, 'orders.procesando', {'cantidad' : cont_cabecera, 'lineas': cont_linea} )


      detalle = 'OK' if cont_linea==registros else 'ERROR'

      logger.info('Termina el ciclo de carga de los detalles, contador en %s vs %s del control ' % (cont_linea,registros ) )
      logger.info('Resultado de la carga de detalles %s' % detalle)

  # -------CABECERA-----------------

  buscId =  'customsearch_ad_dm_sales_order' # InternalId 404 # cabecera

  logger.info('conectandose a netsuite - consulta de cabecera %s' % buscId)

  SearchRecordType = clienteNs.salesFactory.TransactionSearchAdvanced(savedSearchScriptId = buscId)  

 
  searchResult = ns.Search(clienteNs, SearchRecordType)

  if searchResult.status.isSuccess and searchResult.totalRecords>0:  

      sId = searchResult.searchId
      paginas = searchResult.totalPages
      registros = searchResult.totalRecords
      logger.info('El registro de control de netsuite indica %s registros' % registros)
  

      query =  """
         insert into ns_ordenes_cabecera (
            num_documento        
          , num_transaccion   
          , internalId   
          , fecha                
          , cliente_internalId    
          , cliente_identific    
          , fecha_creacion       
          , usuario              
          , ubicacion            
          , tipo                 
          , importe_bruto        
          , cod_descuento       
          , importe_descuento    
          , creador              
          , fecha_creacion2      
          , abono                
          , tipo_factura         
          , nota                 
          , importe_neto         
          , fecha_entrega        
          , hora_entrega         
          , estado 
          , ruc
          , dv
          , nombre
          , email
          , id_tel
          , impuesto
          , cant_lineas


                  ) 
                  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
      logger.info('Inicia el ciclo de carga con el contador en %s' % cont_cabecera  )

      logger.info('Truncando la tabla cabecera en MySQL')
      clienteMomi.cursor.execute ('truncate table ns_ordenes_cabecera')
      

      logger.info('Iniciando ciclo de carga en MySQL')
      for rec in searchResult.searchRowList.searchRow:
          cont_cabecera +=1

          num_doc = nz(rec.basic, ['tranId','searchValue'])

          #OJO depende de que en efecto vengan con el tipo datetime (y no esten nulos)
          fecha_entrega = getCustomField(rec.basic,'custbody_ad_dm_date_delivery', ['searchValue'])
          fecha_entrega = fecha_entrega.astimezone() if fecha_entrega != None else None  
          hora_entrega  = getCustomField(rec.basic,'custbody_ad_pa_delivery_time', ['searchValue'])
          hora_entrega  = hora_entrega.astimezone() if hora_entrega != None else None 
          total = nz(rec.basic, ['total','searchValue'])
          
          fecha_hora_entrega = None
          if fecha_entrega != None and hora_entrega != None:
            fecha_hora_entrega = datetime.combine(fecha_entrega.date(), hora_entrega.time())

          args = (
               num_doc #documento
             , nz(rec.basic, ['transactionNumber','searchValue']) #transaccion
             , nz(rec.basic, ['internalId', 'searchValue','internalId']) #internal de la orden
             , nz(rec.basic, ['tranDate','searchValue'])
             , nz(rec.customerMainJoin, ['internalId','searchValue', 'internalId'])
             , getCustomField(rec.basic, 'custbody_ad_pa_identification', ['searchValue'])
             , nz(rec.basic, ['dateCreated','searchValue'])             
             , getCustomField(rec.basic, 'custbody_adc_usuario', ['searchValue','internalId'])
             , getCustomField(rec.basic,'custbody_ad_pa_store', ['searchValue', 'internalId'])
             , nz(rec.basic, ['type','searchValue'])
             , total
             , nz(rec.basic, ['promoCode','searchValue','internalId']) #tipo descuento
             , None # monto descuento (no se recibe actualmente)
             , nz(rec.basic, ['createdBy','searchValue', 'internalId'])
             , nz(rec.basic, ['dateCreated','searchValue'])             
             , nz(rec.applyingTransactionJoin,['amount','searchValue'] ) #Abono
             , nz(rec.basic, ['customForm','searchValue', 'internalId']) #tipo de factura
             , nz(rec.basic, ['memoMain','searchValue'])
             , nz(rec.basic, ['netAmountNoTax','searchValue'])
             , fecha_entrega
             , fecha_hora_entrega
             , nz(rec.basic, ['status','searchValue']) 
             , getCustomField(rec.customerMainJoin,'custentity_ad_pa_id_number', ['searchValue']) #RUC
             , getCustomField(rec.customerMainJoin,'custentity_ad_pa_control_digits', ['searchValue']) #DV
             , nz(rec.customerMainJoin,['altName','searchValue']) #Nombre del cliente
             , nz(rec.customerMainJoin,['email','searchValue'])
             , nz(rec.customerMainJoin,['entityId','searchValue']) #id/telefono
             , nz(rec.basic, ['taxTotal', 'searchValue'])  
             , None #lineas (no se recibe por ahora)

          

          )

          clienteMomi.cursor.execute (query, args)
          logger.info('se cargo el documento %s - transacc. %s' % (args[0], args[1]))
          clienteMomi.connection.commit ()

          if cont_cabecera % 5 == 0:
             util.transmitir(socket, 'orders.procesando', {'cantidad' : cont_cabecera, 'lineas': cont_linea} )

      cabecera = 'OK' if cont_cabecera==registros else 'ERROR'

      logger.info('Termina el ciclo de carga de la cabecera, contador en %s vs %s en el registro de control de netsuite ' % (cont_cabecera,registros ) )
      logger.info('Resultado de la carga de cabecera %s' % cabecera)

# -----------------------

      logger.info('Resultado del proceso de carga: %s ' % 'OK' if cabecera=='OK' and detalle=='OK' else 'ERROR')


if __name__ == "__main__":
   main()
  
