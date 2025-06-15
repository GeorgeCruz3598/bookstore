from database import db
#from flask_login import UserMixin

class State(db.Model):
    __tablename__ = 'states'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False) 
   
    def __init__(self, name, description):
        self.name = name
        self.description = description 

    @staticmethod
    def get_all():
        return State.query.all()
    
    
    @staticmethod
    def get_by_id(id):
        return State.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return State.query.filter_by(name = name).first()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    def update(self,name=None, description=None):
        #use sucesive conditioned by None default value ifs because logued user is critical
        if name:   
            self.name = name 
        if description:
            self.description = description
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    
    
        
        

