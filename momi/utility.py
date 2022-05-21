import json
import psutil  ## pip install psutil
import os, sys


def transmitir(socket, nombre, mensaje):
    if socket != None:
      x = json.dumps({'data': mensaje })
      socket.emit( nombre, x )
    return


def persistir(engine, session, clase, **valores):
  
    clase.__table__.create(engine, checkfirst=True) 
    
    registro = clase(**valores) 
    session.add(registro)
    session.commit()


def existe_instancia(label="default"):

    myname = sys.argv[0]
    mypid = os.getpid()

    for process in psutil.process_iter():
        if process.pid != mypid:
            for path in process.cmdline():
                if myname in path:
                    print ('process {} found!'.format(myname))
                    #process.terminate()
                    already_running = True      
                    return True             

    return False