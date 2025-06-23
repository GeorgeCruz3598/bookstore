from flask import Flask, render_template, request
from logmanagerconfig import login_manager
from database import db

import os
#from flask_migrate import Migrate

from controllers import user_controller, payment_controller, category_controller, state_controller, provider_controller
from controllers import contact_controller, book_controller, purchase_controller, order_controller

from models.book_model import Book
from models.category_model import Category

app = Flask(__name__)
app.config['SECRET_KEY'] = '20d2995509ff4357692e8c421f3f81b876b0b2391dc84108fd34d86edc33201a'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookstore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#upload file image
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads', 'covers')#storage location
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB maximo
os.makedirs(UPLOAD_FOLDER, exist_ok=True) #ensure it exists

#login manager
login_manager.init_app(app)

# db init
db.init_app(app)

#migrate = Migrate(app,db) 

# BluePrints
app.register_blueprint(user_controller.user_bp)
app.register_blueprint(payment_controller.payment_bp)
app.register_blueprint(category_controller.category_bp)
app.register_blueprint(state_controller.state_bp)
app.register_blueprint(provider_controller.provider_bp)
app.register_blueprint(contact_controller.contact_bp)
app.register_blueprint(book_controller.book_bp)
app.register_blueprint(purchase_controller.purchase_bp)
app.register_blueprint(order_controller.order_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return(dict(is_active = is_active)) 

#Para tener disponible la lista de categorias activas en cualquier lugar del pryecto
@app.context_processor
def inject_categories():
    categories = Category.get_all_active()
    return dict(categories=categories)

@app.route("/")#entry points
@app.route("/home")
def index():
    books = Book.get_first_10_active()
    return render_template('index.html',books=books, title="Libros Destacados")

@app.route("/all_books")
def index_all():
    books = Book.get_all_active()
    return render_template('index_all.html',books=books, title="Todos los Libros")

@app.route("/where_we_are")
def map():
    return render_template("map.html")

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)