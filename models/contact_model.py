from database import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.Text, nullable = False) 
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    user_relation = db.relationship('User', back_populates='contacts_relation')
    
    def __init__(self, message,user_id):
        self.message = message
        self.user_id = user_id 

    @staticmethod
    def get_all():
        return Contact.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Contact.query.get(id)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    #Admins solo podran listar y eliminar -> no editar
    def update(self,message=None, user_id=None):
        if message:   
            self.message = message 
        if user_id:
            self.user_id = user_id
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
    
    
        
        

