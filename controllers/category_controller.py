from flask import redirect, flash, request, url_for, Blueprint
from flask_login import login_required, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User

from models.category_model  import Category
from views import category_view
from forms.form_categories import CreateForm, EditForm

from database import db

category_bp = Blueprint('category', __name__, url_prefix='/categories')

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@category_bp.route("/")
#@admin_required
def index():
    categories = Category.get_all()
    return category_view.list(categories=categories)

@category_bp.route("/admin/create", methods=['POST','GET'])
@admin_required #if not flash + redirect to run.index 
def create():
    form = CreateForm()
    if form.validate_on_submit():
        name =  form.name.data
        description = form.description.data
        is_active = form.is_active.data
        
        category = Category(name, description, is_active)
        try:
            category.save() # commit the creation
            flash("Successfully Added","success")
            return redirect(url_for('category.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return category_view.create(form=form)
         
@category_bp.route("/admin/edit/<int:id>", methods= ['POST','GET'])
@admin_required
def edit(id):
    category = Category.get_by_id(id)
    form = EditForm(obj=category)
    if form.validate_on_submit():
        form.populate_obj(category)        
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('category.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return category_view.edit(form=form, category=category)

@category_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    category = Category.get_by_id(id)
    category.delete()
    flash("Succesfully Removed","success")
    return redirect(url_for('category.index'))
