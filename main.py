# Flask Libraries
from flask import render_template

# App Modules
from app import create_app
from app.forms import SearchForm

app = create_app() #Iniciamos la aplicacion de Flask


@app.route('/',  methods=['GET', 'POST'])
def index():
    search_form = SearchForm()

    context = {
        'search_form': search_form
    }

    if search_form.validate_on_submit():
        # Realizamos la tarea de busqueda.
        print(search_form.searchbar.data)
        print('Realizamos la busqueda')

    return render_template('index.html', **context)

