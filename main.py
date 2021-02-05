# Flask Libraries
from flask import render_template

# flaskr Libraries
from flaskr import create_app

app = create_app() #Iniciamos la aplicacion de Flask


@app.route('/')
def index():
    return render_template('index.html', duro="Hola")

