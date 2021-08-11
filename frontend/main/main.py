from flask import Blueprint, render_template, request, redirect
#from flask import current_app as app

from sqlalchemy import Table, Column, Integer, func, sql


from datetime import datetime

import sqlalchemy

from ..models import OrdenesCabecera, Todo, vResumenItemActual, vResumenItemAnterior , VentasPendientes, Registro
from ..models import vResumenOrdenesActual

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
 
    resumen = vResumenOrdenesActual().query.first_or_404()
    tabla = db.session.query(OrdenesCabecera).filter(OrdenesCabecera.proc_status=="KO").order_by(OrdenesCabecera.fecha.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)    

    if request.method == "POST":
        pass
    else:
        return render_template('ordenes.html', datos=resumen, tabla=tabla)



@main_bp.route('/cash', methods=['GET', 'POST'])
def cash():

    #TODO: mejorar en un solo query
    resumen = db.session.query( func.count(VentasPendientes.rcp_pedido).label('cantidad'), 
                             func.sum(VentasPendientes.rcp_monto).label('monto'),
                             ).first()

    totl = resumen.cantidad or 0
    monto = resumen.monto or 0
    facs = db.session.query(VentasPendientes.rcp_pedido).filter(VentasPendientes.rcp_salida=='FA').count()
    devs = db.session.query(VentasPendientes.rcp_pedido).filter(VentasPendientes.rcp_salida=='NC').count()
    otrs = totl-facs-devs    

    antes = { 'totl':totl, 'facs':facs, 'devs':devs, 'otrs':otrs, 'monto':monto}


    ok = db.session.query(Registro.rcp_pedido).filter(Registro.reg_estatus=='OK').count()
    ko = db.session.query(Registro.rcp_pedido).filter(Registro.reg_estatus=='KO').count()
    fec = db.session.query(func.max(Registro.reg_fecha_modificacion).label('fec')).one_or_none()

    print('respuesta... ', type(fec))

    #print ('valor de respuesta...',fec.strftime("%Y-%m-%d %H:%M:%S.%f"))

    procs = ok+ko
    pends = totl - procs
    
    actual = { 'totl':procs, 'facs':ok, 'devs':ko, 'otrs':0, 'fec':fec}
    fec2 = db.session.query()

    if request.method == "POST":
        pass
        #task.content = request.form['content']
    else:
        return render_template('venta_contado.html', antes=antes, actual=actual, flag=False)


@main_bp.route('/credit', methods=['GET', 'POST'])
def credit():

    #task = Todo.query.get_or_404(id)

    if request.method == "POST":
        pass
        #task.content = request.form['content']
    else:
        return render_template('venta_credito.html', fecha=fecha_sistema())

