from concurrent.futures.thread import _python_exit
from flask import redirect, flash, request, url_for, Blueprint
from flask_login import login_required, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User

from models.provider_model  import Provider
from views import provider_view
from forms.form_providers import CreateForm, EditForm

from database import db

provider_bp = Blueprint('provider', __name__, url_prefix='/providers')

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@provider_bp.route("/")
#@admin_required
def index():
    providers = Provider.get_all()
    return provider_view.list(providers=providers)

@provider_bp.route("/admin/create", methods=['POST','GET'])
@admin_required #if not flash + redirect to run.index 
def create():
    form = CreateForm()
    if form.validate_on_submit():
        name =  form.name.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        is_active = form.is_active.data
        
        provider = Provider(name,email,phone,address, is_active)
        try:
            provider.save() # commit the creation
            flash("Successfully Added","success")
            return redirect(url_for('provider.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return provider_view.create(form=form)
         
@provider_bp.route("/admin/edit/<int:id>", methods= ['POST','GET'])
@admin_required
def edit(id):
    provider = Provider.get_by_id(id)
    form = EditForm(obj=provider) # populate form fields with same name object fields
    if form.validate_on_submit():
        form.populate_obj(provider)       #store changes 
        try:
            db.session.commit() #commit changes in DB
            flash("Succesfully Updated", "success")
            return redirect(url_for('provider.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return provider_view.edit(form=form, provider=provider)

@provider_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    provider = Provider.get_by_id(id)
    provider.delete()
    flash("Succesfully Removed","success")
    return redirect(url_for('provider.index'))
