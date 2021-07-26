from time import monotonic
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import Table 

from . import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Task %r' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100)) 
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __repr__(self):
        return 'User %r' % self.id



#------- VISTAS -------

class vResumenItemAnterior(db.Model):
    __tablename__ = 'vi_resumen_item_ant'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    terminado = db.Column(db.Integer)
    ensamblado = db.Column(db.Integer)
    kit = db.Column(db.Integer)
    fecha = db.Column(db.String)



class vResumenItemActual(db.Model):
    __tablename__ = 'vi_resumen_item_act'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    terminado = db.Column(db.Integer)
    ensamblado = db.Column(db.Integer)
    kit = db.Column(db.Integer)
    fecha = db.Column(db.String)


class vResumenOrdenesActual(db.Model):
    __tablename__ =  'vi_resumen_ordenes_act'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    lineas   = db.Column(db.Integer)
    ubicaciones = db.Column(db.Integer)
    monto = db.Column(db.Integer)
    clientes = db.Column(db.Integer)


class VentasPendientes (db.Model):
    #reflejando la vista 
    __table__ = db.Table('vi_ventas_pendientes', db.metadata  
                           , db.Column('rcp_pedido',  primary_key=True)
                           , autoload_with=db.engine
                   )

class Registro (db.Model):
    #reflejando la vista 
    __table__ = db.Table('registro', db.metadata  
                           , db.Column('rcp_cia',  primary_key=True)
                           , db.Column('rcp_pedido',  primary_key=True)
                           , autoload_with=db.engine
                   )