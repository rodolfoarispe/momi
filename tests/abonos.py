#---incluir parent dir----
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#------------------------

from datetime import datetime

import dbConn as db
from momi import regAbono

db.Base.metadata.create_all(db.engine) #se crean las tablas

session = db.Session()

rcpedidos = db.Table ('rcpedidos', db.metadata, autoload=True, autoload_with=db.engine)

data = regAbono()
data.num_orden = 1
data.num_abono = "ABO.01"
data.monto = 100
data.fecha = datetime.now()
session.add(data)
session.commit()

dato = session.query(regAbono).first()
print (dato.num_orden)
