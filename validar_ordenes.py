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
  

  logger.info('--- VALIDACION DE ORDENES ---')

  logger.info('Crendo cliente para MySQL')
  clienteMomi = DataBaseClient(connect=True) 
  util.transmitir(socket, 'orders.mensajes', 'Inicia proceso de Validación de las ordenes')
  util.transmitir(socket, 'orders.mensajes', 'Conexión a MySQL... OK')

  clienteMomi.connection.autocommit = True #queremos que insert cada sentencia ejecutada      

  # CONTADORES
  cont_cabecera = 0
  cont_linea = 0


  cursor1 = clienteMomi.cursor
  cursor2 = clienteMomi.getCursor()

  util.transmitir(socket, 'orders.mensajes', 'Revisando las ordenes...')


  query1 =  """
            select 
                  internalId 
                , num_documento 
                , importe_bruto
                , fecha
                , creador 
            from ns_ordenes_cabecera 
            order by 2,1

           """

  cursor1.execute (query1)
  records = cursor1.fetchall()

  for rec in records:
      
      cont_cabecera+=1
            
      num_id = rec[0]
      num_doc = rec[1]
      total = rec[2]
      fecha = rec[3]
      creador = rec[4]

      p_stat = 'ok'
      p_desc = ''
      p_err = []

      # =============

      #validar duplicados

      cursor2.execute(" select count(*) from ns_ordenes_cabecera where num_documento = '{}' ".format(num_doc))
      if cursor2.fetchone()[0] >1:
          p_err.append( 'Cabecera con numero de documento duplicado') 

      #validar monto y lineas
      cursor2.execute ("select count(*) cant, sum(importe_bruto) monto from ns_ordenes_detalle where num_documento ='{}'".format(num_doc) )
      res = cursor2.fetchone()
      lineas = res[0]
      bruto = res[1]

      if lineas == 0:
        p_err.append( 'La cabecera no tiene lineas de detalle') 

      if abs(bruto - total) > 0.01:
        p_err.append('Total de la cabecera difiere del total del detalle')


      # validaciones temporales
      if fecha < datetime(2021,6,1):
         p_err.append('Anterior a la fecha de corte de prueba (jul.21')

      if creador != '39611':
        p_err.append('No fue creado por usuario de pruebas (Adan Rueda')

      # ==================
      
        
      if len(p_err)>0:
        p_stat = "KO"
        p_desc = '. '.join(p_err) 

      query2 = """
                update ns_ordenes_cabecera set 
                         proc_status = '{}'
                       , proc_descr = '{}'
                       , cant_lineas = {} 
                where internalId = '{}'
                
                """
      cursor2.execute(query2.format(p_stat, p_desc, lineas, num_id))
      logger.info('Procesado el registro {} con num.doc {} -> {}'.format(cont_cabecera, num_doc, p_stat))

  logger.info('Termina el proceso de validación')
  util.transmitir(socket, 'orders.mensajes', 'Terminó el proceso de validación!')

if __name__ == "__main__":
   main()

