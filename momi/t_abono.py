from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.sql.expression import true
#from sqlalchemy.sql.sqltypes import Date, Numeric

import dbConn as db

class regAbono(db.Base):
    __tablename__ = 'abonos'

    num_orden = Column( Integer, primary_key=True)
    num_abono = Column( String(10), primary_key=True)
    fecha     = Column ( Date)
    monto     = Column(Float)

            
