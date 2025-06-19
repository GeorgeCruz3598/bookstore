from flask import redirect, flash, request, url_for, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from decorators import admin_required
from logmanagerconfig import login_manager

from models.user_model import User
from models.order_model import Order

from views import user_view

from forms.form_users import CreateForm, LoginForm, EditForm

from database import db

user_bp = Blueprint('user', __name__, url_prefix='/users')

#login manager
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) 

@user_bp.route("/")
@admin_required
def index():
    users = User.get_all()
    return user_view.list(users=users)

@user_bp.route("/admin/create", methods=['POST','GET'])
@admin_required #if not flash + redirect to "/"
def create():
    form = CreateForm()
   
    if 'cancel' in request.form:
        return redirect(url_for('user.index'))
    
    if form.validate_on_submit():

        name =  form.name.data
        username = form.username.data
        passwd = form.passwd.data
        is_admin = form.is_admin.data
        email = form.email.data
        phone = form.phone.data
        
        user = User(name,username, passwd, is_admin,email,phone)
        try:
            user.save()
            flash("Successfully Added, please log in","success")
            return redirect(url_for('user.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot Create, Error:{e}", "danger")
    return user_view.create(form=form)
         
@user_bp.route("/admin/edit/<int:id>", methods= ['POST','GET'])
@admin_required
def edit(id):
    user = User.get_by_id(id)
    form = EditForm(obj=user)
    
    if 'cancel' in request.form:
        return redirect(url_for('user.index'))
    
    if form.validate_on_submit() or request.method == 'POST':
        if form.cancel.data:
            return redirect(url_for('user.index'))
        form.populate_obj(user)        
        # isolated process for password
        passwd = request.form.get('passwd')
        user.update_pass(passwd=passwd)
        try:
            db.session.commit()
            flash("Succesfully Updated", "success")
            return redirect(url_for('user.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Cannot update, Error:{e}", "danger")
    return user_view.edit(form=form, user=user)

@user_bp.route("/admin/delete/<int:id>", methods=['POST','GET'])
@admin_required
def delete(id):
    user = User.get_by_id(id)
    orders_count = Order.get_by_user_id_count(id)
    if orders_count > 0:
        flash(f"No se puede eliminar el usuario '{user.username}'({user.name}) porque tiene {orders_count} pedidos asociados."
                f"\tPor favor, elimine o reasigne los pedidos antes de proseguir. ",'danger') #danger
        return redirect(url_for('order.index'))
    user.delete()
    flash("Succesfully Removed","success")
    return redirect(url_for('user.index'))

@user_bp.route("/signup", methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        flash('You are already in, you cannot signup',"warning")
        return redirect(url_for('index'))
    form = CreateForm()
   
    if 'cancel' in request.form:
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        passwd = form.passwd.data
        email = form.email.data
        phone = form.phone.data
        
        user = User(name=name,username=username,passwd=passwd,is_admin=False,email=email,phone=phone)
        try:
            user.save()
            flash("Succesfully Registered, please Log in", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Cannot Sign Up, an Error was detected: {e}',"danger")
    return user_view.signup(form=form)

@user_bp.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in',"warning")
        return redirect(url_for('index'))
    form = LoginForm()
    
    if 'cancel' in request.form:
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        
        user = User.get_by_username(form.username.data)
        if user and user.verify_passwd(form.passwd.data):
            login_user(user)
            flash("Succesfully Logged","success")
            return redirect(url_for('index'))
        else:
            flash("User or Password not valid !","danger")
    return user_view.login(form=form)

@user_bp.route("/logout",methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash("Successfully Logged Out","warning")
    return redirect(url_for('index'))