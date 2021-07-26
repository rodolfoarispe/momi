
"""
Prueba de devolucion de venta contado 

"""

#-- agregando el directorio padre
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#----


import devol_contado_put as devol
import momi.t_cabecera as cab
import momi.t_detalle as det 


from datetime import datetime, timedelta 

#CABECERA
master = cab.regCabecera()
details = []

secuencial = datetime.now().strftime("%y%m%d%H%M%S")

master.num_cuenta     = None
master.num_factura    = 'TEST-' + secuencial
master.fecha_transacc = datetime(2021,4,20)
master.estatus        = 4 #??
master.cod_ubicacion  =  1
master.cod_cliente    = 39841 #cliente anonimo
master.cod_fiscal     = 'ABCXYZ-' + secuencial
#master.cod_vendedor   = 7202
#master.metodo_pago = 5

#ARTICULOS  


item1 = det.regDetalle()
item1.cantidad     = 2
item1.cod_articulo = 2820
item1.descripcion  = 'PANETELITA'
item1.linea        = 1
item1.location     = 1
item1.precio       = 1.50
details.append(item1) 

#item2 = det.regDetalle()
#item2.cantidad     = None
#item2.cod_articulo = 2198
#item2.descripcion  = 'desc dulc 20%'
#item2.linea        = item1.linea + 1
#item2.location     = item1.location
#item2.precio       = item1.precio * 0.20
#details.append(item2) 


try:
    resp = devol.subirDevolucionContado (master, details)
    
    internal =  resp.get('internalId') if resp.get('isSuccess') == 'true' else 'Err'

    for x in resp.get('mensajes'):
        print('%s / internal: %s -> %s: %s ' % (  master.num_factura,  internal  , x.get('codigo') ,  x.get('mensaje')))
except Exception as e:
    print (e.args[0])