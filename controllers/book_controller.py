from flask import redirect, flash, request, url_for, Blueprint, current_app
from flask_login import login_required, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User
from models.purchase_model import Purchase
from models.category_model import Category
from models.order_model import Order

from models.book_model  import Book
from views import book_view
from forms.form_books import CreateForm, EditForm

from database import db

#para manejo de archivos
import os
import uuid
#from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage #verificar si es File


book_bp = Blueprint('book', __name__, url_prefix='/books')

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@book_bp.route("/")
@admin_required
def index():
    books = Book.get_all()
    return book_view.list(books=books)  #para usuario normal eria solo activos
    
@book_bp.route("/admin/create", methods=['POST','GET'])
@admin_required 
def create():
    form = CreateForm()
    
    if 'cancel' in request.form:
        return redirect(url_for('book.index'))
    
    if form.validate_on_submit():
        if form.category_id.data == 0:
            flash('Por favor, selecciona una categoría válida.', 'warning')
            return redirect(url_for('book.create'))
        if form.state_id.data == 0:
            flash('Por favor, selecciona un estado válido.', 'warning')
            return redirect(url_for('book.create'))
        
        title = form.title.data
        author = form.author.data
        description = form.description.data
        language = form.language.data
        price = form.price.data
        category_id = form.category_id.data #retrieve value=id
        state_id = form.state_id.data #retrieve value=id
        is_active = form.is_active.data
                
        #Image path
        # Generar un nombre de archivo único
        random_hex = str(uuid.uuid4())
        _, f_ext = os.path.splitext(form.cover.data.filename)
        image_filename = random_hex + f_ext
        picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
        # Guardar el archivo en el sistema de archivos
        form.cover.data.save(picture_path) 
        cover = image_filename
        
        book = Book (title=title,author=author,description=description,language=language,price=price,stock=0,category_id=category_id,state_id=state_id,cover=cover,is_active=is_active)
        
        
        try:
            book.save() # commit the creation
            flash("Successfully Added","success")
            return redirect(url_for('book.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return book_view.create(form=form)
         
@book_bp.route("/admin/edit/<int:id>", methods= ['POST','GET'])
#@admin_required
def edit(id):
    book = Book.get_by_id(id)
    form = EditForm(obj=book)
    
    if 'cancel' in request.form:
        return redirect(url_for('book.index'))
    
    #we make it explicitly to ensure cover path is reseted to NOne when try to select or not a  new file
    if request.method=='GET': 
        form.cover.data = None
    
    if form.validate_on_submit():
        if form.category_id.data == 0:
            flash('Por favor, selecciona una categoría válida.', 'warning')
            return redirect(url_for('book.edit'))
        if form.state_id.data == 0:
            flash('Por favor, selecciona un estado válido.', 'warning')
            return redirect(url_for('book.edit'))
           
        #update Cover
        if isinstance(form.cover.data, FileStorage): 
            
            if form.cover.data: #si hay nuevo book cover en edicion
                if book.cover: #se borra el cover existente
                    old_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.cover)
                    if os.path.exists(old_picture_path):
                        os.remove(old_picture_path)
                # se crea nuevo cover 
                random_hex = str(uuid.uuid4())
                _, f_ext = os.path.splitext(form.cover.data.filename)
                image_filename = random_hex + f_ext
                picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                form.cover.data.save(picture_path)
                #Save cover_path in DB
                book.cover = image_filename # filename
                
        title = form.title.data
        author = form.author.data
        description = form.description.data
        language = form.language.data
        price = form.price.data
        category_id = form.category_id.data
        state_id = form.state_id.data
        is_active = form.is_active.data
        
        book.update(title=title,author=author, description=description,language=language,price=price, category_id=category_id, state_id=state_id, is_active=is_active)
        
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('book.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return book_view.edit(form=form, book=book)

@book_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    book = Book.get_by_id(id)
    purchase_count = Purchase.get_by_book_id_count(id)
    orders_count = Order.get_by_book_id_count(id)
    
    if orders_count > 0:
        flash(f"No se puede eliminar el usuario '{book.title}' porque tiene {orders_count} pedidos asociados."
                f"\tPor favor, elimine o reasigne los pedidos antes de proseguir. ",'danger') #danger
        return redirect(url_for('order.index'))
    elif purchase_count > 0:
        flash(f"No se puede eliminar el libro '{book.title}' porque tiene {purchase_count} compras asociadas."
              f"\tPor favor, elimine o reasigne las compras antes de proseguir. ",'danger') #danger
        return redirect(url_for('purchase.index'))
    else:
        if book.cover:
            old_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], book.cover)
            if os.path.exists(old_picture_path):
                os.remove(old_picture_path)
        book.delete()
        flash("Succesfully Removed","success")
    return redirect(url_for('book.index'))

@book_bp.route("/books_by_category/<int:category_id>")
def books_by_category(category_id):
    books = Book.get_by_category_all_active(category_id)
    category = Category.get_by_id(category_id)
    return book_view.list_by_category_active(books=books, category=category)

