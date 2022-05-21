
"""
Prueba de depositos a ordenes
"""

#-- agregando el directorio padre
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#----

from deposito_orden_put import subirAbono
from momi.t_abono import regAbono

from datetime import datetime, timedelta 

secuencial = datetime.now().strftime("%y%m%d%H%M%S")

#CABECERA
master = regAbono()

master.num_abono = 3
master.num_pedido = 'PE271' 
master.num_documento = 30273
master.fecha = datetime(2021,9,5)
master.monto = 39.50 
master.metodo_pago = 1


try:
    resp = subirAbono (master)
    
    internal =  resp.get('internalId') if resp.get('isSuccess') == 'true' else 'Err'

    for x in resp.get('mensajes'):
        print('%s / internal: %s -> %s: %s ' % (  master.num_factura,  internal  , x.get('codigo') ,  x.get('mensaje')))
except Exception as e:
    print (e.args[0])