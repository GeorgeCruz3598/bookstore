
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Length, DataRequired, Email

class CreateForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired(),Length(max=64)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    phone = StringField('Telefono',validators=[DataRequired()])
    address = StringField('Direccion',validators=[DataRequired()])
    is_active = BooleanField('Activo')
    
    submit = SubmitField('Registrar')
    cancel = SubmitField('Cancelar')
    

class EditForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired(),Length(max=64)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    phone = StringField('Telefono',validators=[DataRequired()])
    address = StringField('Direccion',validators=[DataRequired()])
    is_active = BooleanField('Activo')
    
    submit = SubmitField('Editar')
    cancel = SubmitField('Cancelar')
