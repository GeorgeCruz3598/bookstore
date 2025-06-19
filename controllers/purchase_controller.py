#from decimal import Decimal

from flask import redirect, flash, url_for, Blueprint, request
from flask_login import login_required
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User
from models.book_model import Book
from models.provider_model import Provider

from models.purchase_model  import Purchase
from views import purchase_view
from forms.form_purchases import CreateForm, EditForm

from database import db

purchase_bp = Blueprint('purchase', __name__, url_prefix='/purchases')

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@purchase_bp.route("/")
@admin_required
def index():
    purchases = Purchase.get_all()
    return purchase_view.list(purchases=purchases)

@purchase_bp.route("/admin/create", methods=['POST','GET'])
@admin_required 
def create():
    form = CreateForm()
    
    if 'cancel' in request.form:
        return redirect(url_for('purchase.index'))    
    
    if form.validate_on_submit():
        if form.book_id.data == 0:
            flash('Por favor, selecciona un libro válido.', 'warning')
            return redirect(url_for('purchase.create'))
        if form.provider_id.data == 0:
            flash('Por favor, selecciona un proveedor válido.', 'warning')
            return redirect(url_for('purchase.create'))
        
        quantity = form.quantity.data
        detail = form.detail.data
        book_id = form.book_id.data #retrieve value=id
        provider_id = form.provider_id.data #retrieve value=id
        
        #manage total
        book = Book.get_by_id(book_id)
        total = float(book.price)* quantity
           
        purchase = Purchase(quantity=quantity,detail=detail, total=total,book_id = book_id, provider_id=provider_id)
        #manage stock
        book.increment_stock(quantity)
        try:
            purchase.save() # commit the creation
            flash("Successfully Added","success")
            return redirect(url_for('purchase.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return purchase_view.create(form=form)
         
@purchase_bp.route("/admin/edit/<int:id>", methods= ['POST','GET'])
@admin_required
def edit(id):
    purchase = Purchase.get_by_id(id)
    
    book = Book.get_by_id(purchase.book_id)
    provider = Provider.get_by_id(purchase.provider_id)
    
    quantity_before = purchase.quantity    
        
    form = EditForm(obj=purchase) #carga los datos con los fieldnames que coinciden form.detail.data = purchase.detail
    
    if 'cancel' in request.form:
        return redirect(url_for('purchase.index'))
    
    if form.validate_on_submit():            
        quantity = form.quantity.data #new quantity                
        detail = form.detail.data #new detail
        
        if quantity == quantity_before: #solo cambio detail y stock no cambia
            purchase.set_detail(detail)
        else:            
            stock_prueba = book.stock - quantity_before + quantity
            if stock_prueba >= 0:    
                purchase.set_detail(detail)
                purchase.set_quantity(quantity)
                book.set_stock(stock_prueba) #update stock                
            else: 
                flash("No se puede actualizar la cantidad de la compra porque no se tiene suficiente stock de libros","danger")
                return redirect(url_for('purchase.index'))
            
        #manage total
        total = float(book.price) * quantity
        purchase.set_total(total)
        
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('purchase.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return purchase_view.edit(form=form, purchase=purchase, book=book, provider = provider)

@purchase_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    purchase = Purchase.get_by_id(id)
    book = Book.get_by_id(purchase.book_id)
    
    if book.stock > 0 and book.stock >= purchase.quantity:
        book.decrement_stock(purchase.quantity)
        purchase.delete()
        flash("Succesfully Removed","success")
    else:
        flash(f"No se puede eliminar la compra porque no se tienen suficientes  libros (stock{book.stock})","danger")
    return redirect(url_for('purchase.index'))