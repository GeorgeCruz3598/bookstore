from flask import redirect, flash, request, url_for, Blueprint
from flask_login import login_required, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User
from models.book_model import Book

from models.state_model  import State
from views import state_view
from forms.form_states import CreateForm, EditForm

from database import db

state_bp = Blueprint('state', __name__, url_prefix='/states')

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@state_bp.route("/")
#@admin_required
def index():
    states = State.get_all()
    return state_view.list(states=states)

@state_bp.route("/admin/create", methods=['POST','GET'])
@admin_required #if not flash + redirect to run.index 
def create():
    form = CreateForm()
    
    if 'cancel' in request.form:
            return redirect(url_for('state.index'))
        
    if form.validate_on_submit():
        name =  form.name.data
        description = form.description.data
        
        state = State(name, description)
        try:
            state.save() # commit the creation
            flash("Successfully Added","success")
            return redirect(url_for('state.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return state_view.create(form=form)
         
@state_bp.route("/admin/edit/<int:id>", methods= ['POST','GET'])
@admin_required
def edit(id):
    state = State.get_by_id(id)
    form = EditForm(obj=state)
    
    if 'cancel' in request.form:
            return redirect(url_for('state.index'))
        
    if form.validate_on_submit():
        form.populate_obj(state)        
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('state.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return state_view.edit(form=form, state=state)

@state_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    state = State.get_by_id(id)
    book_count = Book.get_by_state_id_count(id)
    if book_count > 0 :
        flash(f"No se puede eliminar el estado '{state.name}' porque tiene {book_count} libros asociados."
              f"\tPor favor, elimine o reasigne los libros antes de proseguir. ",'danger') #danger
        return redirect(url_for('book.index'))
    else:
        state.delete()
        flash("Succesfully Removed","success")
        return redirect(url_for('state.index'))
