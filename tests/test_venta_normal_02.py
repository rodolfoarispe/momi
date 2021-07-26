
"""
Prueba de venta contado con vendor asignado

"""

#-- agregando el directorio padre
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#----


import venta_contado_put as venta
import momi.t_cabecera as cab
import momi.t_detalle as det 


from datetime import datetime, timedelta 

#CABECERA
master = cab.regCabecera()
details = []

secuencial = datetime.now().strftime("%y%m%d%H%M%S")

master.num_cuenta     = None
master.num_factura    = 'TEST-' + secuencial
master.fecha_transacc = datetime(2021,7,22)
master.estatus        = 4 #??
master.cod_ubicacion  =  1
master.cod_cliente    = 39841 #cliente venta contado
master.cod_fiscal     = 'ABCXYZ-' + secuencial
master.cod_vendedor   = 39861 #vendedor punto de venta
master.metodo_pago1 = 1


#ARTICULOS  


item1 = det.regDetalle()
item1.cantidad     = 2
item1.cod_articulo = 13222
item1.descripcion  = 'cake vainilla 7'
item1.linea        = 1
item1.location     = 1
item1.precio       = 12.95
details.append(item1) 

item2 = det.regDetalle()
item2.cantidad     = None
item2.cod_articulo = 2198
item2.descripcion  = 'desc dulc 20%'
item2.linea        = item1.linea + 1
item2.location     = item1.location
item2.precio       = item1.precio * 0.20
#details.append(item2) 


try:
    resp = venta.subirVentaContado (master, details)
    
    internal =  resp.get('internalId') if resp.get('isSuccess') == 'true' else 'Err'

    for x in resp.get('mensajes'):
        print('%s / internal: %s -> %s: %s ' % (  master.num_factura,  internal  , x.get('codigo') ,  x.get('mensaje')))
except Exception as e:
    print (e)