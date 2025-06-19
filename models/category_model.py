
from database import db
#from flask_login import UserMixin

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False) 
    is_active = db.Column(db.Boolean, default = True)
   
    books_relation = db.relationship('Book', back_populates='category_relation')
    
    def __init__(self, name, description, is_active):
        self.name = name
        self.description = description 
        self.is_active = is_active 

    @staticmethod
    def get_all():
        return Category.query.all()
    
    @staticmethod
    def get_all_active():
        return Category.query.filter(Category.is_active == True).order_by(Category.name).all()
    
    @staticmethod
    def get_by_id(id):
        return Category.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Category.query.filter_by(name = name).first()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    def update(self,name=None, description=None, is_active=None):
        #use sucesive conditioned by None default value ifs because logued user is critical
        if name:   
            self.name = name 
        if description:
            self.description = description
        if is_active:
            self.is_active = is_active
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    
    
        
        

