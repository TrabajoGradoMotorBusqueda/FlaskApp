# Modulo Ontologia
import inspect
import os
import sys

# Flask Libraries
from flask import render_template

# App Modules
from app import create_app
from app.forms import SearchForm

# UIMI Modules
import uimi

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(1, current_dir + '/ontologia')

app = create_app()  # Iniciamos la aplicacion de Flask


@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()

    context = {
        'search_form': search_form
    }

    if search_form.validate_on_submit():
        # Realizamos la tarea de busqueda.
        print(search_form.searchbar.data)
        resultado = uimi.search_engine(search_form.searchbar.data)
        resultado = list(map(str, resultado))
        return ' '.join(resultado)

    return render_template('index.html', **context)
