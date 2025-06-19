from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Length, DataRequired

class CreateForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired(),Length(max=64)])
    description = TextAreaField('Descripcion',validators=[DataRequired()])
    is_active = BooleanField('Activo')
    submit = SubmitField('Registrar')
    cancel = SubmitField('Cancelar')

class EditForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired(),Length(max=64)])
    description = TextAreaField('Descripcion',validators=[DataRequired()])
    is_active = BooleanField('Activo')
    submit = SubmitField('Editar')
    cancel = SubmitField('Cancelar')
    