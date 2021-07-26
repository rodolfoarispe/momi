import time 
import json
from flask_socketio import SocketIO, emit
from .. import socketio

from .. import proc_items
from .. import proc_orders

@socketio.on('proceso')
def handle_my_custom_event(input_json):
    opcion =  input_json.get('data')

    if opcion == 'items':
        txt = 'Iniciando el proceso: ' + opcion + '<br>La descarga puede tomar varios minutos.<br>Por favor espere...'
        emit ('items.procesando', json.dumps({'data': {'cantidad':0}}))
        emit ('items.mensajes', json.dumps({'data': txt}) ) 

        x = proc_items.main(socketio)

        socketio.start_background_task(target=x)  
        
        #time.sleep(5)
        emit ('items.procesado', json.dumps({'data':'Proceso Terminado!<br>La p&aacute;gina se refresacar&aacute; en segundos' }) )

    if opcion == 'orders':
        txt = 'Iniciando el proceso: ' + opcion + '<br>La descarga puede tomar varios minutos.<br>Por favor espere...'
        emit ('orders.procesando', json.dumps({'data': {'cantidad':0, 'lineas':0}}))
        emit ('orders.mensajes', json.dumps({'data': txt}) ) 

        x = proc_orders.main(socketio)

        socketio.start_background_task(target=x)  
        
        #time.sleep(5)
        emit ('orders.procesado', json.dumps({'data':'Proceso Terminado!<br>La p&aacute;gina se refresacar&aacute; en segundos' }) )


