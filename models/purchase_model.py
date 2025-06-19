from database import db
from datetime import datetime

class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key = True)
    quantity = db.Column(db.Integer, nullable = False, default = 0)
    detail = db.Column(db.Text, nullable = False) 
    total = db.Column(db.Float(10,2), nullable = False, default = 0.0) 
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable = False) #with foreign table name
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable = False)
    create_at = db.Column(db.DateTime, default=datetime.now)
   
    book_relation = db.relationship('Book', back_populates='purchases_relation')
    provider_relation = db.relationship('Provider', back_populates='purchases_relation')
    
    def __init__(self, quantity, detail, total, book_id, provider_id):
        self.quantity = quantity #in forms will be validated to be > 0
        self.detail = detail
        self.total = total
        self.book_id = book_id
        self.provider_id = provider_id
        
    def set_total(self,total):
        self.total = total
        
    def set_quantity(self,quantity=None):
        if quantity:
            self.quantity = quantity
            
    def set_detail(self,detail=None):
        if detail:
            self.detail = detail
            
    @staticmethod
    def get_all():
        return Purchase.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Purchase.query.get(id)
    
    @staticmethod
    def get_by_book_id_count(book_id):
        return Purchase.query.filter_by(book_id = book_id).count()

    @staticmethod
    def get_by_provider_id_count(provider_id):
        return Purchase.query.filter_by(provider_id = provider_id).count()
    
    #not used beacuse we'll use: form.populate()          
    def update(self, quantity = None, detail = None, total=None, book_id=None, provider_id=None):
        if quantity is not None:
            self.quantity = quantity 
        if detail is not None:
            self.detail = detail
        if total is not None: 
            self.total = total
        if book_id is not None:
            self.book_id = book_id
        if provider_id is not None: 
            self.provider_id = provider_id   
        #db.session.commit()
   
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    
    
    
        
    
        
        


