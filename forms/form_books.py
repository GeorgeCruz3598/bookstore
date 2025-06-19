from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField, DecimalField
from wtforms.validators import Length, DataRequired, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

#For selectors
from models.category_model import Category
from models.state_model import State


class CreateForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    description = TextAreaField('Sinopsis', validators=[DataRequired(message="Este campo no puede  estar vacio")])
    language = SelectField('Idioma', choices=[
        ('item','Seleccionar un Idioma'),
        ('Español','Español'),
        ('Ingles','Ingles'),
        ('Frances','Frances'),
        ('Aleman','Aleman'),
        ('Otro','Otro')], validators=[DataRequired()])
    
    price = DecimalField('Precio(Bs.)', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    #stock = IntegerField('') #NO se añade se incrementa con la compras
    
    category_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    state_id = SelectField('Estado', coerce=int, validators=[DataRequired()])
    
    cover = FileField('Portada del Libro', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo se permiten imágenes (jpg, png, jpeg, gif)!'),
        FileRequired("Porfavor, suba una imagen de la portada!")]) 
    
    is_active = BooleanField('Activo')
    
    submit = SubmitField('Guardar')
    cancel = SubmitField('Cancelar')
        
    #init options for selectors
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(0, 'Seleccione una categoria')] + [(c.id, c.name) for c in Category.get_all_active()]
        self.state_id.choices = [(0, 'Seleccione un Estado')] + [(s.id, s.name) for s in State.get_all()]

class EditForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    description = TextAreaField('Sinopsis', validators=[DataRequired(message="Este campo no puede  estar vacio")])
    language = SelectField('Idioma', choices=[
        ('item','Seleccionar un Idioma'),
        ('Español','Español'),
        ('Ingles','Ingles'),
        ('Frances','Frances'),
        ('Aleman','Aleman'),
        ('Otro','Otro')], validators=[DataRequired()])
    
    price = DecimalField('Precio(Bs.)', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    #stock = IntegerField('') #NO se añade se incrementa con la compras
    
    category_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    state_id = SelectField('Estado', coerce=int, validators=[DataRequired()])
    
    cover = FileField('Portada del Libro', validators=[ Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo se permiten imágenes (jpg, png, jpeg, gif)!')
        ]) 
    
    is_active = BooleanField('Activo')
    
    submit = SubmitField('Editar')
    cancel = SubmitField('Cancelar')
    #init options for selectors
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(0, 'Seleccione una categoria')] + [(c.id, c.name) for c in Category.get_all_active()]
        self.state_id.choices = [(0, 'Seleccione un Estado')] + [(s.id, s.name) for s in State.get_all()]