from database import db
from datetime import datetime

class Provider(db.Model):
    __tablename__ = 'providers'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    is_active = db.Column(db.Boolean, default = False)
    
    
    def __init__(self, name,  email, phone, address, is_active):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.is_active = is_active
  
    @staticmethod
    def get_all():
        return Provider.query.all()
    
    @staticmethod
    def get_all_active():
        return Provider.query.filter(Provider.is_active == True).all()
    
    @staticmethod
    def get_by_id(id):
        return Provider.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Provider.query.filter_by(name = name).first()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    
    
        
        

