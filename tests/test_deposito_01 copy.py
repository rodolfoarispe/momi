
"""
Prueba de depositos de cliente
"""

#-- agregando el directorio padre
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#----

from deposito_cliente_put import subirPago
from momi.t_cabecera import regCabecera

from datetime import datetime, timedelta 

secuencial = datetime.now().strftime("%y%m%d%H%M%S")

#CABECERA
master = regCabecera()

master.num_factura = 'DEP-' + secuencial
master.monto_pago1 = 100
master.fecha_transacc = datetime(2021,4,20)
master.cod_cliente = 39841 
master.metodo_pago1 = 1

master.estatus = True  # booleano para fondo sin depositar
#master.cod_ubicacion  =  1
#master.cod_cliente    = 12 #cliente anonimo

try:
    resp = subirPago (master)
    
    internal =  resp.get('internalId') if resp.get('isSuccess') == 'true' else 'Err'

    for x in resp.get('mensajes'):
        print('%s / internal: %s -> %s: %s ' % (  master.num_factura,  internal  , x.get('codigo') ,  x.get('mensaje')))
except Exception as e:
    print (e.args[0])