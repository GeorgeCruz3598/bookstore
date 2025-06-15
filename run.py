from flask import Flask, render_template, redirect, url_for
from logmanagerconfig import login_manager
from database import db

from controllers import user_controller, payment_controller, category_controller, state_controller, provider_controller

app = Flask(__name__)
app.config['SECRET_KEY'] = '20d2995509ff4357692e8c421f3f81b876b0b2391dc84108fd34d86edc33201a'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookstore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#login manager
login_manager.init_app(app)

# db init
db.init_app(app)

#migrate = Migrate() -> defined en otro .py
#migrate.init_app()

# BluePrints
app.register_blueprint(user_controller.user_bp)
app.register_blueprint(payment_controller.payment_bp)
app.register_blueprint(category_controller.category_bp)
app.register_blueprint(state_controller.state_bp)
app.register_blueprint(provider_controller.provider_bp)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)