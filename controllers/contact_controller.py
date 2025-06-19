from flask import redirect, flash, request, url_for, Blueprint
from flask_login import login_required, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User

from models.contact_model  import Contact
from views import contact_view
from forms.form_contacts import CreateForm

from database import db

contact_bp = Blueprint('contact', __name__, url_prefix='/contacts')

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@contact_bp.route("/")
@admin_required
def index():
    contacts = Contact.get_all()
    return contact_view.list(contacts=contacts)

#only user
@contact_bp.route("/create", methods=['POST','GET'])
@login_required
def create():
    form = CreateForm()
    
    if 'cancel' in request.form:
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        message =  form.message.data
        user_id = current_user.id
        contact = Contact(message=message, user_id=user_id)
        try:
            contact.save() # commit the creation
            flash("Message Successfully Sent","success")
            return redirect(url_for('index')) # go to main page
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Send, Error:{e}", "danger")
    return contact_view.create(form=form)

#olyadmin        
@contact_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    contact = Contact.get_by_id(id)
    contact.delete()
    flash("Succesfully Removed","success")
    return redirect(url_for('contact.index')) #go to dashboard
