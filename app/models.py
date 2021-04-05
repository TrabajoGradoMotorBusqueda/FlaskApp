# from sqlalchemy import Column, Integer, String, Text, ARRAY
from main import db


class DiccionarioLema(db.Model):
    __tablename__ = 'diccionario_lema'
    lema = db.Column(db.String(500), primary_key=True, nullable=False)
    palabras = db.Column(db.ARRAY(db.String(500)))

    def __init__(self, lema, palabras):
        self.lema = lema
        self.palabras = palabras

    def agregar_palabras(self, palabras):
        self.palabras = palabras

    def __repr__(self):
        return f'DiccionarioLema({self.lema} => {self.palabras})'

    def __str__(self):
        return self.lema


class Investigacion(db.Model):
    __tablename__ = 'resumenes_investigacion'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_investigacion = db.Column(db.String(8))
    titulo_investigacion = db.Column(db.String(10000))
    resumen_investigacion = db.Column(db.Text)
    estado_investigacion = db.Column(db.String(100))
    palabra_clave1 = db.Column(db.String(500))
    palabra_clave2 = db.Column(db.String(500))
    palabra_clave3 = db.Column(db.String(500))
    palabra_clave4 = db.Column(db.String(500))
    palabra_clave5 = db.Column(db.String(500))
    convocatoria = db.Column(db.String(100))
    tipo_convocatoria = db.Column(db.String(100))
    anio_convocatoria = db.Column(db.Integer)
    codigo_autor1 = db.Column(db.Integer)
    nombres_autor1 = db.Column(db.String(100))
    apellidos_autor1 = db.Column(db.String(100))
    programa_autor1 = db.Column(db.String(500))
    facultad_autor1 = db.Column(db.String(500))
    departamento_autor1 = db.Column(db.String(500))
    grupo_investigacion1 = db.Column(db.String(500))
    linea_investigacion1 = db.Column(db.String(500))
    codigo_autor2 = db.Column(db.Integer)
    nombres_autor2 = db.Column(db.String(100))
    apellidos_autor2 = db.Column(db.String(100))
    programa_autor2 = db.Column(db.String(500))
    facultad_autor2 = db.Column(db.String(500))
    departamento_autor2 = db.Column(db.String(500))
    grupo_investigacion2 = db.Column(db.String(500))
    linea_investigacion2 = db.Column(db.String(500))
    codigo_autor3 = db.Column(db.Integer)
    nombres_autor3 = db.Column(db.String(100))
    apellidos_autor3 = db.Column(db.String(100))
    programa_autor3 = db.Column(db.String(500))
    facultad_autor3 = db.Column(db.String(500))
    departamento_autor3 = db.Column(db.String(500))
    grupo_investigacion3 = db.Column(db.String(500))
    linea_investigacion3 = db.Column(db.String(500))
    codigo_autor4 = db.Column(db.Integer)
    nombres_autor4 = db.Column(db.String(100))
    apellidos_autor4 = db.Column(db.String(100))
    programa_autor4 = db.Column(db.String(500))
    facultad_autor4 = db.Column(db.String(500))
    departamento_autor4 = db.Column(db.String(500))
    grupo_investigacion4 = db.Column(db.String(500))
    linea_investigacion4 = db.Column(db.String(500))
    asesor1 = db.Column(db.String(100))
    asesor2 = db.Column(db.String(100))
    asesor3 = db.Column(db.String(100))
    asesor4 = db.Column(db.String(100))
    tipo_resumen = db.Column(db.String(20))
    corpus = db.Column(db.Text)
    corpus_palabras = db.Column(db.Text)
    corpus_lemas = db.Column(db.Text)

    def __init__(self, values=None):
        if values is None:
            return
        for attribute in values.keys():
            setattr(self, attribute, values[attribute])

    def __attributes_setter__(self, values):
        for attribute in values.keys():
            setattr(self, attribute, values[attribute])

    def __repr__(self):
        return f'ResumenDocente({self.titulo_investigacion}, {self.convocatoria})'

    def __str__(self):
        return self.titulo_investigacion
