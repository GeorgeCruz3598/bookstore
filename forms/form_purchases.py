from flask_wtf import FlaskForm

from wtforms import HiddenField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import Length, DataRequired, NumberRange, Optional

#For selectors
from models.book_model import Book
from models.provider_model import Provider

class CreateForm(FlaskForm):
    quantity = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1, message="La cantidad debe ser mayor a 0.")])
    detail = TextAreaField('Detalles Adicionales', validators=[DataRequired(message="Este campo no puede  estar vacio")])    
    #total = DecimalField('Total', validators=[DataRequired()], places=2)
    book_id = SelectField('Libro', coerce=int, validators=[DataRequired()])
    provider_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
        
    #init options for selectors
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.book_id.choices = [(0, 'Seleccione un libro')] + [(b.id, b.title) for b in Book.get_all_active()]
        self.provider_id.choices = [(0, 'Seleccione un Proveedor')] + [(p.id, p.name) for p in Provider.get_all_active()]

class EditForm(FlaskForm):
    quantity = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1, message="La cantidad debe ser mayor a 0.")])
    detail = TextAreaField('Detalles Adicionales', validators=[DataRequired(message="Este campo no puede  estar vacio")])    
    submit = SubmitField('Editar')
    cancel = SubmitField('Cancelar')