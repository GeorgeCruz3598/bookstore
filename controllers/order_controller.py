#from decimal import Decimal

from flask import redirect, flash, url_for, Blueprint, request
from flask_login import login_required, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.payment_model import Payment
from models.user_model import User
from models.book_model import Book

from models.order_model  import Order
from views import order_view
from forms.form_orders import CreateForm, EditForm

from database import db

order_bp = Blueprint('order', __name__, url_prefix='/orders')

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@order_bp.route("/")
@admin_required
def index():
    orders = Order.get_all()
    return order_view.list(orders=orders)

@order_bp.route("admin/edit/<int:id>", methods= ['POST','GET'])
@admin_required
def edit(id):
    order = Order.get_by_id(id)
    book = Book.get_by_id(order.book_id)
    quantity_before = order.quantity    
        
    form = EditForm(obj=order) #carga los datos con los fieldnames que coinciden form.detail.data = purchase.detail
    
    if 'cancel' in request.form:
        return redirect(url_for('order.index'))
    
    if form.validate_on_submit():            
        if form.payment_id.data == 0:
            flash('Por favor, selecciona un Metodo de Pago válido.', 'warning')
            return redirect(url_for('order.edit',id=id))
        
        quantity = form.quantity.data #new quantity                
        payment_id = form.payment_id.data
        
        if quantity == quantity_before: #solo cambia metodo de pago y stock no cambia
            order.set_payment_id(payment_id)
        else:            
            stock_prueba = book.stock + quantity_before - quantity
            if stock_prueba >= 0:    
                order.set_payment_id(payment_id)
                order.set_quantity(quantity)
                book.set_stock(stock_prueba) #update stock                
            else: 
                flash(f"No se puede editar la cantidad del pedido porque no se tiene suficiente stock ({book.stock} libros)","danger")
                return redirect(url_for('order.index'))
            
        #manage total
        total = float(book.price) * quantity
        order.set_total(total)
        
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('order.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return order_view.edit(form=form, order=order, book=book)

@order_bp.route("admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    order = Order.get_by_id(id)
    book = Book.get_by_id(order.book_id)
    book.increment_stock(order.quantity)
    order.delete()
    flash("Succesfully Removed","success")
    return redirect(url_for('order.index'))
    
@order_bp.route("/my_orders")
@login_required
def my_orders():
    orders = Order.get_by_user_id(current_user.id)
    return order_view.my_orders(orders=orders)

@order_bp.route("/add_order/<int:book_id>", methods=['POST','GET'])
@login_required 
def add_order(book_id):
    book = Book.get_by_id(book_id)
    form = CreateForm()

    if 'cancel' in request.form:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        if form.payment_id.data == 0:
            flash('Por favor, selecciona un Metodo de Pago válido.', 'warning')
            return redirect(url_for('order.add_order',book_id=book_id))
        
        quantity = form.quantity.data
        payment_id = form.payment_id.data
        
        #manage total
        total = float(book.price) * quantity
        
        #manage stock
        if book.stock > 0 and book.stock >= quantity:  
            order = Order(quantity=quantity,total=total,user_id = current_user.id,payment_id = payment_id,book_id=book_id) 
            book.decrement_stock(quantity)            
        else: 
            flash(f"No se puede realizar el pedido porque no se tiene suficiente stock ({book.stock} libros)","danger") 
            return redirect(url_for('order.add_order',book_id=book_id))
        
        try:
            order.save() # commit the creation
            flash("Successfully Added","success")
            return redirect(url_for('order.my_orders'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return order_view.add_order(form=form, book=book)
         
@order_bp.route("my_orders/edit/<int:id>", methods= ['POST','GET'])
@login_required
def my_orders_edit(id):
    order = Order.get_by_id(id)
    book = Book.get_by_id(order.book_id)
    
    quantity_before = order.quantity    
        
    form = EditForm(obj=order) #carga los datos con los fieldnames que coinciden form.detail.data = purchase.detail
  
    if 'cancel' in request.form:
            return redirect(url_for('order.my_orders'))
  
    if form.validate_on_submit():            
        if form.payment_id.data == 0:
            flash('Por favor, selecciona un Metodo de Pago válido.', 'warning')
            return redirect(url_for('order.my_orders_edit',id=id))
        
        quantity = form.quantity.data #new quantity                
        payment_id = form.payment_id.data
        
        if quantity == quantity_before: #solo cambia metodo de pago y stock no cambia
            order.set_payment_id(payment_id)
        else:            
            stock_prueba = book.stock + quantity_before - quantity
            if stock_prueba >= 0:    
                order.set_payment_id(payment_id)
                order.set_quantity(quantity)
                book.set_stock(stock_prueba) #update stock                
            else: 
                flash(f"No se puede editar la cantidad del pedido porque no se tiene suficiente stock ({book.stock} libros)","danger")
                return redirect(url_for('order.my_orders'))
            
        #manage total
        total = float(book.price) * quantity
        order.set_total(total)
        
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('order.my_orders'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
            
    return order_view.my_orders_edit(form=form, order=order, book=book)

@order_bp.route("my_orders/delete/<int:id>", methods=['POST','GET'])
@login_required
def my_orders_delete(id):
    order = Order.get_by_id(id)
    book = Book.get_by_id(order.book_id)
    book.increment_stock(order.quantity)
    order.delete()
    flash("Succesfully Removed","success")
    return redirect(url_for('order.my_orders'))