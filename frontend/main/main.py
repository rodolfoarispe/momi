from flask import Blueprint, render_template, request, redirect
#from flask import current_app as app

from sqlalchemy import Table, Column, Integer, func, sql, and_


from datetime import datetime

import sqlalchemy

from ..models import OrdenesCabecera, Todo, vResumenItemActual, vResumenItemAnterior , Registro
from ..models import vResumenOrdenesActual, rcPedidos, rdPedidos

from .. import db


main_bp = Blueprint('main_bp', __name__, template_folder='templates')

def fecha_sistema(): 
  return datetime.now().strftime("%d-%b-%Y, %I:%M %p")


@main_bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
    #    task_content = request.form['content']
    #    new_task = Todo(content=task_content)

        try:
            
    #        db.session.add(new_task)
    #        db.session.commit()
            return redirect('/')
        except:
            return 'Error adding'

    else:
        #tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('dashboard.html', fecha=fecha_sistema())



@main_bp.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting'


@main_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
    else:
        return render_template('update.html', task=task)

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Error updating'


@main_bp.route('/items', methods=['GET', 'POST'])
def items():

    resumen_ant = vResumenItemAnterior().query.first_or_404()
    resumen_act = vResumenItemActual().query.first_or_404()

    if request.method == "POST":
        #task.content = request.form['content']
        pass ;
    else:
        return render_template('inventario.html',  
                    antes=resumen_ant, actual=resumen_act )



@main_bp.route('/orders', methods=['GET', 'POST'])
def orders():

    ROWS_PER_PAGE = 20

    page = request.args.get('page',1, type=int)
    tab = request.args.get('tab', 1, type=int)
 
    resumen = vResumenOrdenesActual().query.first_or_404()

    tabla = None 

    if tab==1:
       tabla = db.session.query(OrdenesCabecera).filter(OrdenesCabecera.proc_status=="ok").order_by(OrdenesCabecera.fecha.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)    

    if tab==2:
       tabla = db.session.query(OrdenesCabecera).filter(OrdenesCabecera.proc_status=="KO").order_by(OrdenesCabecera.fecha.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)    

    if request.method == "POST":
        pass
    else:
        return render_template('ordenes.html', datos=resumen, tabla=tabla, tab=tab)



@main_bp.route('/cash', methods=['GET', 'POST'])
def cash():

    ROWS_PER_PAGE = 20
    page = request.args.get('page',1, type=int)
    tab = request.args.get('tab', 1, type=int)    

    # INI: se construyen los queries
    ped_reg = db.session.query(rcPedidos, Registro).join(Registro, and_ (rcPedidos.rcp_cia == Registro.rcp_cia   
                                                , rcPedidos.rcp_pedido == Registro.rcp_pedido), 
                                                isouter=True ).subquery()  

    q1 = db.session.query(ped_reg).filter(ped_reg.c.reg_estatus==None).subquery() #pendientes
    q2 = db.session.query(ped_reg).filter(ped_reg.c.reg_estatus=='OK').subquery() #aceptados
    q3 = db.session.query(ped_reg).filter(ped_reg.c.reg_estatus=='KO').subquery() #rechazados
    q4 = db.session.query(ped_reg).filter(ped_reg.c.reg_estatus!=None).subquery() #procesados

    # INI: se construyen los queries

    resumen = db.session.query(func.count(q1.c.rcp_pedido).label('cantidad'), 
                               func.sum(q1.c.rcp_monto).label('monto')
                               ).one_or_none()

    totl = resumen.cantidad or 0
    monto = resumen.monto or 0

    facs = db.session.query(q1).filter(q1.c.rcp_salida == 'FA').count()
    devs = db.session.query(q1).filter(q1.c.rcp_salida == 'NC').count()
    otrs = totl-facs-devs    

    antes = { 'totl':totl, 'facs':facs, 'devs':devs, 'otrs':otrs, 'monto':monto}

    #ok = db.session.query(Registro.rcp_pedido).filter(Registro.reg_estatus=='OK').count()
    ok  = db.session.query(q2).count()
    #ko = db.session.query(Registro.rcp_pedido).filter(Registro.reg_estatus=='KO').count()
    ko  = db.session.query(q3).count()
    fec = db.session.query(func.max(Registro.reg_fecha_modificacion).label('fec')).one_or_none().fec

    
    qry = None
    if tab ==1: qry = q1
    if tab ==2: qry = q2 
    if tab ==3: qry = q3 
    

    tabla = db.session.query(qry).order_by(qry.c.reg_fecha_creacion).paginate(page=page, per_page=ROWS_PER_PAGE)    

    mnt = db.session.query(func.sum(q4.c.rcp_monto).label('mnt')).one_or_none().mnt

    procs = ok+ko
    pends = totl - procs
    
    actual = { 'totl':procs, 'facs':ok, 'devs':ko, 'otrs':0,  'monto':mnt, 'fec':fec}
    #fec2 = db.session.query()


    if request.method == "POST":
        pass
        #task.content = request.form['content']
    else:
        return render_template('venta_contado.html', antes=antes, actual=actual, tabla=tabla, page=page, tab=tab, flag=False)


@main_bp.route('/credit', methods=['GET', 'POST'])
def credit():

    #task = Todo.query.get_or_404(id)

    if request.method == "POST":
        pass
        #task.content = request.form['content']
    else:
        return render_template('venta_credito.html', fecha=fecha_sistema())

