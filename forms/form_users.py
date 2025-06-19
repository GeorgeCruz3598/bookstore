from calendar import day_abbr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Length, DataRequired, Email

class CreateForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired(),Length(max=64)])
    username = StringField('Username',validators=[DataRequired(),Length(max=20)])
    passwd = PasswordField('Contraseña',validators=[DataRequired()])
    is_admin = BooleanField('Administrador')
    email = StringField('Email',validators=[DataRequired(), Email()])
    phone = StringField('Telefono',validators=[DataRequired()])
    submit = SubmitField('Registrar')
    cancel = SubmitField('Cancelar')
    
class EditForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired(),Length(max=64)])
    username = StringField('Username',validators=[DataRequired(),Length(max=20)])
    is_admin = BooleanField('Administrador')
    email = StringField('Email',validators=[DataRequired(), Email()])
    phone = StringField('Telefono',validators=[DataRequired()])
    submit = SubmitField('Editar')
    cancel = SubmitField('Cancelar')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    passwd = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Aceptar')
    cancel = SubmitField('Cancelar')