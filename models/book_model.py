
from database import db
from datetime import datetime
from flask import flash

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable = False) 
    language = db.Column(db.String(20), nullable= False)
    price = db.Column(db.Float, nullable = False, default = 0.0)
    stock = db.Column(db.Integer, nullable = False, default = 0)
    
    #El manejo de error ante el borrado de tabla padre se hara en el controller de categories y states
    #no se aplica borrado automatico como en contactanos
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable = False)
    
    cover = db.Column(db.String(255),nullable=False) 
    create_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)
    is_active = db.Column(db.Boolean, default = True)
   
    category_relation = db.relationship('Category', back_populates='books_relation')
    state_relation = db.relationship('State', back_populates='books_relation')
    
    purchases_relation = db.relationship('Purchase', back_populates='book_relation')
    orders_relation = db.relationship('Order', back_populates='book_relation')
    
    def __init__(self, title, author, description, language,price, stock, category_id,state_id, cover,is_active):
        self.title = title
        self.author = author
        self.description = description
        self.language = language
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.state_id = state_id
        self.cover = cover
        self.is_active = is_active

    @staticmethod
    def get_all():
        return Book.query.all()
    
    @staticmethod
    def get_first_10_active():
        return Book.query.filter(Book.is_active == True).order_by(Book.title).limit(10).all()
    
    @staticmethod
    def get_all_active():
        return Book.query.filter(Book.is_active == True).all()
    
    @staticmethod
    def get_by_category_all_active(category_id):
        return Book.query.filter(Book.category_id == category_id,Book.is_active ==True).order_by(Book.title).all()
    
    @staticmethod
    def get_by_id(id):
        return Book.query.get(id)
    
    @staticmethod
    def get_by_author(author):
        return Book.query.filter_by(author = author).first()
    
    @staticmethod
    def get_by_category_id_count(category_id):
        return Book.query.filter_by(category_id = category_id).count()

    @staticmethod
    def get_by_state_id_count(state_id):
        return Book.query.filter_by(state_id = state_id).count()

    #Stock Manage
    def increment_stock(self,quantity):
        self.stock = (self.stock or 0) + quantity
        
    def decrement_stock(self,quantity):
        if (self.stock > 0 or not None) and (self.stock >= quantity):
            self.stock -= quantity
            
    def reset_stock(self):
        self.stock = 0
        
    def set_stock(self,stock):
        self.stock = stock
    ######
    
    def update_cover(self,cover=None):
        if cover:
            self.cover = cover
                      
    def update(self,title=None, author=None, description=None, language=None, price=None, category_id=None, state_id=None,is_active=None):
        if title is not None:
            self.title = title 
        if author is not None:
            self.author = author
        if description is not None: 
            self.description = description
        if language is not None:
            self.language = language
        if price is not None: 
            self.price = price
        if category_id is not None:
            self.category_id = category_id
        if state_id is not None:
            self.state_id = state_id
        if is_active is not None: #se usa not None para evitar confusioncon el valor is_Active = false -> nunca se guardaria enDB
            self.is_active = is_active
            
        #db.session.commit()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    
        
    
        
        


