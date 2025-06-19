
from database import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Integer, nullable = False, default = 0)
    total = db.Column(db.Float, nullable = False, default = 0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    user_relation = db.relationship('User', back_populates='orders_relation')
    payment_relation = db.relationship('Payment', back_populates='orders_relation')
    book_relation = db.relationship('Book', back_populates='orders_relation')

    def __init__(self, quantity, total, user_id,payment_id,book_id):
        self.quantity = quantity
        self.total = total
        self.user_id = user_id
        self.payment_id = payment_id
        self.book_id = book_id

    @staticmethod
    def get_all():
        return Order.query.order_by(Order.created_at).all()
    
    @staticmethod
    def get_by_user_id(user_id):
        return Order.query.filter_by(user_id = user_id).order_by(Order.created_at).all()
    
    @staticmethod
    def get_by_id(id):
        return Order.query.get(id)
    
    @staticmethod
    def get_by_user_id_count(user_id):
        return Order.query.filter_by(user_id = user_id).count()

    @staticmethod
    def get_by_payment_id_count(payment_id):
        return Order.query.filter_by(payment_id = payment_id).count()
    
    @staticmethod
    def get_by_book_id_count(book_id):
        return Order.query.filter_by(book_id = book_id).count()

    def set_total(self,total=None):
        if total is not None:
            self.total = total
            
    def set_payment_id(self,payment_id=None):
        if payment_id is not None:
            self.payment_id = payment_id
            
    def set_quantity(self,quantity=None):
        if quantity is not None:
            self.quantity = quantity
            
    def update(self,quantity=None, payment_id=None): 
        if quantity is not None:
            self.quantity = quantity       
        if payment_id is not None:
            self.payment_id = payment_id
        #db.session.commit()
        
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    
        
    
        
        



