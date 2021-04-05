"""
Forms Busquedas
"""

from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired

# WTForms


# class LoginForm(FlaskForm):
#     """docstring for LoginForms"""
#     username = StringField('Nombre de Usuario', validators=[DataRequired()])
#     password = PasswordField('Contraseña', validators=[DataRequired()])
#     submit = SubmitField('Enviar')


class SearchForm(FlaskForm):
    searchbar = SearchField('', validators=[DataRequired()])
    submit = SubmitField('Buscar')

