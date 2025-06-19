
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import Length, DataRequired

class CreateForm(FlaskForm):
    message = TextAreaField('Mensaje',validators=[DataRequired(message="el mensaje no puede estar vacio")])
    user_id = HiddenField('User_ID')
    submit = SubmitField('Registrar')
    cancel = SubmitField('Cancelar')