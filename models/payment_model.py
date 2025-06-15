from database import db
#from flask_login import UserMixin

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False) 
    is_active = db.Column(db.Boolean, default = True)
   
    def __init__(self, name, description, is_active):
        self.name = name
        self.description = description 
        self.is_active = is_active 

    @staticmethod
    def get_all():
        return Payment.query.all()
    
    @staticmethod #added
    def get_all_active():
        return Payment.query.filter(Payment.is_active == True).all()
    
    @staticmethod
    def get_by_id(id):
        return Payment.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Payment.query.filter_by(name = name).first()

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
            
    
    
        
        

