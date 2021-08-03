import json

def transmitir(socket, nombre, mensaje):
  if socket != None:
     x = json.dumps({'data': mensaje })
     socket.emit( nombre, x )
  return

def getValue(objeto, propiedad):
   if hasattr(objeto, propiedad):
      return objeto.get(propiedad)   
   return propiedad
