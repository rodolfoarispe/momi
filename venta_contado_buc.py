

from mysql.connector import connect
from venta_contado_get import leerVentaContado, buscarVentasContado
from venta_contado_put import subirVentaContado
from devol_contado_put import subirDevolucionContado
from venta_contado_reg import registrarVentaContado
from momi import regCabecera, regDetalle, DataBaseClient
from netsuite import NetSuiteClient 
from momi import utility as util

from time import sleep
from datetime import datetime, timedelta 
import locale
import sys

print ('\nInterface de Integración POS-Netsuite')

# OJO: se crean las variables a nivel del módulo para que existan desde la importación y esten disponibles globalmente a otros modulos
nsClient = NetSuiteClient() #usaaremos esta conexión 
dbClient = DataBaseClient() 

def Procesar( grupo, socket=None):


  
    print ('\nCreando cliente Netsuite...', end='')
    nsClient.Connect()
    print('OK') #se crea un cliente para usarlo durante todo el bucle
    util.transmitir(socket, 'cashsale.mensajes', 'Cliente Netsuite... OK')
    print ('Creando cliente de la Base de Datos...', end='')   
    dbClient.Connect()
    print ('OK') #se crea un cliente de la base de datos
    util.transmitir(socket, 'cashsale.mensajes', 'Cliente MySQL... OK')

    try:

        cnx = dbClient.connection 
        dbClient.cursor = buscarVentasContado(cnx, grupo) # cargas el cursor con los datos
        util.transmitir(socket, 'cashsale.mensajes', 'Buscando registros tipo {}...'.format(grupo))

        #if dbClient.cursor.rowcount > 0: print ('\n')
        
        cont_ok = 0
        cont_ko = 0

        for row in dbClient.cursor:
            registro = dict(zip(dbClient.cursor.column_names, row))
            data = leerVentaContado(cnx,  registro )
            
            maestro:regCabecera = data['cabecera']
            detalle:regDetalle  = data['detalle']

            if maestro == None:
                return 

            #-- carga a Netsuite OJO: solo acepta los tipos FA y NC

            respuesta = {'isSuccess' : 'false',
                         'mensajes': [],
                         'internalId': None }

            if maestro.tipo_registro == 'FA':
                respuesta = subirVentaContado(maestro, detalle, nsClient)

            else:
                if maestro.tipo_registro == 'NC':
                    respuesta = subirDevolucionContado(maestro, detalle, nsClient)
                else:
                    respuesta ['isSuccess'] = 'false'
                    respuesta['mensajes'] = [{'tipo' :'CASHSALE', 'codigo':'ERROR', 'mensaje': 'El tipo de registros debe ser FA o NC'}]

            if  respuesta['isSuccess'] == 'true':
                cont_ok += 1
            else:
                cont_ko +=1 

            util.transmitir(socket, 'cashsale.procesando', {'aceptados' : cont_ok, 'rechazados': cont_ko} )

            #-- registrar resultado
            registrarVentaContado(maestro.num_cia, maestro.num_factura, respuesta) 


        return 
        
    except Exception as e:
        print (e)
        return False


def bucle():
    delta = timedelta(minutes=60) #tiempo para reintentar con los fallidos
    then = datetime(1969,2,14) #se forza una fecha del pasado la primera vez

    while True:
        print ('Buscando registros nuevos...', end='')
        print (datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        Procesar ('NW')  #nuevos
        sleep(1)
        current = datetime.now()
        if (current - then).total_seconds() > delta.total_seconds(): #si ha pasado suficiente tiempo
            #print ('Buscando registros rechazados...')
            #procesar(dbClient, 'KO')  #reintentar rechazados
            then = datetime.now()
            #print ('Ciclo completado.  el proceso reiniciará en un minuto...')
        print ('Entrando en modo de espera...')
        sleep(60)


if __name__ == '__main__':

    if util.existe_instancia():
        print ('Error.  Ya se esta ejecutando una instancia del programa')
        sys.exit()

    bucle()