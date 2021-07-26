import json

def transmitir(socket, nombre, mensaje):
  if socket != None:
     x = json.dumps({'data': mensaje })
     socket.emit( nombre, x )
  return
