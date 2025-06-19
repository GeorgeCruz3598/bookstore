from flask import redirect, flash, request, url_for, Blueprint
from flask_login import login_required, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User
from  models.order_model import Order

from models.payment_model  import Payment
from views import payment_view
from forms.form_payments import CreateForm, EditForm

from database import db

payment_bp = Blueprint('payment', __name__, url_prefix='/payments')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@payment_bp.route("/")
#@admin_required
def index():
    payments = Payment.get_all()
    return payment_view.list(payments=payments)

@payment_bp.route("/admin/create", methods=['POST','GET'])
@admin_required #if not flash + redirect to run.index 
def create():
    form = CreateForm()
    
    if 'cancel' in request.form:
        return redirect(url_for('payment.index'))
    
    if form.validate_on_submit():
        name =  form.name.data
        description = form.description.data
        is_active = form.is_active.data
        
        payment = Payment(name, description, is_active)
        try:
            payment.save() # commit the creation
            flash("Successfully Added","success")
            return redirect(url_for('payment.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return payment_view.create(form=form)
         
@payment_bp.route("/admin/edit/<int:id>", methods= ['POST','GET'])
@admin_required
def edit(id):
    payment = Payment.get_by_id(id)
    form = EditForm(obj=payment)
    
    if 'cancel' in request.form:
        return redirect(url_for('payment.index'))
    
    if form.validate_on_submit():
        form.populate_obj(payment)        
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('payment.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return payment_view.edit(form=form, payment=payment)

@payment_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    payment = Payment.get_by_id(id)
    orders_count = Order.get_by_payment_id_count(id)
    if orders_count > 0:
        flash(f"No se puede eliminar el metodo de pago '{payment.name}' porque tiene {orders_count} pedidos asociados."
              f"\tPor favor, elimine o reasigne los pedidos antes de proseguir. ",'danger') #danger
        return redirect(url_for('order.index'))
    else:    
        payment.delete()
        flash("Succesfully Removed","success")
        return redirect(url_for('payment.index'))
