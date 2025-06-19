from database import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(20), nullable = False)
    pass_hash = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now) #utcnow #Date -> date.today  from datetime import date
    is_admin = db.Column(db.Boolean, default = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    
    contacts_relation = db.relationship('Contact', back_populates = 'user_relation', cascade="all, delete-orphan") 
    #lazy='dynamic' permite hacr consultas directamente sobre la relacion - se define aqui
    orders_relation = db.relationship('Order', back_populates = 'user_relation') 
    
    def __init__(self, name, username, passwd, is_admin, email, phone):
        self.name = name
        self.username = username
        self.pass_hash = self.hash_passwd(passwd)
        self.is_admin = is_admin
        self.email = email
        self.phone = phone
        
    def verify_passwd(self, passwd):
        return check_password_hash(self.pass_hash, passwd)
    
    @staticmethod
    def hash_passwd(passwd):
        return generate_password_hash(passwd)

    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username = username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email = email).first()
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    def update(self,name=None, username=None, passwd=None, is_admin=None, email=None, phone=None):
        #use sucesive conditioned by None default value ifs because logued user is critical
        if name:   
            self.name = name 
        if username:
            self.username = username
        if passwd:
            self.pass_hash = self.hash_passwd(passwd)
        if is_admin:
            self.is_admin = is_admin
        if email:
            self.email = email
        if phone:
            self.phone = phone
        db.session.commit()

    def update_pass(self, passwd=None):
        if passwd:
            self.pass_hash = self.hash_passwd(passwd)
        #db.session.commit() #performed in controller
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    
    
        
        

