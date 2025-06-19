from flask_wtf import FlaskForm

from wtforms import HiddenField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import Length, DataRequired, NumberRange, Optional

#For selectors

from models.payment_model import Payment

class CreateForm(FlaskForm):
    quantity = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1, message="La cantidad debe ser mayor a 0.")])
    payment_id = SelectField('Metodo de Pago', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
     
    #init options for selectors
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.payment_id.choices = [(0, 'Seleccione un Metodo de Pago')] + [(p.id, p.name) for p in Payment.get_all_active()]

class EditForm(FlaskForm):
    quantity = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1, message="La cantidad debe ser mayor a 0.")])

    payment_id = SelectField('Metodo de Pago', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Editar')
    cancel = SubmitField('Cancelar')
    
    #init options for selectors
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.payment_id.choices = [(0, 'Seleccione un Metodo de Pago')] + [(p.id, p.name) for p in Payment.get_all_active()]