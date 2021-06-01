# from sqlalchemy import Column, Integer, String, Text, ARRAY
from math import isnan as nan
from app import db


class DiccionarioLema(db.Model):
    __tablename__ = 'diccionario_lema'
    lema = db.Column(db.String(500), primary_key=True, nullable=False)
    palabras = db.Column(db.ARRAY(db.String(500)))

    def __init__(self, lema, palabras):
        self.lema = lema
        self.palabras = palabras

    def __repr__(self):
        return f'DiccionarioLema({self.lema} => {self.palabras})'

    def __str__(self):
        return self.lema

    def save(self, update=False):
        if self.lema is not None and not update:
            db.session.add(self)
        db.session.commit()

    def set_palabras(self, palabras):
        self.palabras = palabras

    def set_lema(self, lema):
        self.lema = lema

    @staticmethod
    def get_by_lema(lema):
        return DiccionarioLema.query.get(lema)

    @staticmethod
    def get_lemas():
        lemas = DiccionarioLema.query.with_entities(DiccionarioLema.lema).all()
        return [lema[0] for lema in lemas]


class Investigacion(db.Model):
    __tablename__ = 'resumenes_investigacion'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_investigacion = db.Column(db.Integer)
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
    corpus_lemas_autores = db.Column(db.Text)

    def __init__(self, values=None):
        if values is None:
            return
        else:
            self.__attributes_setter__(values)

    def __attributes_setter__(self, values):
        if self.id is not None:
            del values['id']
        for attribute in values.keys():
            try:
                value = int(values[attribute]) if not nan(values[attribute]) else None
            except:
                value = values[attribute]
            setattr(self, attribute, value)


    def __save__(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'ResumenDocente({self.titulo_investigacion}, {self.convocatoria})'

    def __str__(self):
        return self.titulo_investigacion

    @staticmethod
    def __get_all__():
        return Investigacion.query.all()

    @staticmethod
    def __get_by_id__(_id_):
        return Investigacion.query.get(_id_)

    @staticmethod
    def __get_by_id_investigacion__(_id_investigacion_):
        return Investigacion.query.filter(Investigacion.id_investigacion == int(_id_investigacion_)).one_or_none()

    @staticmethod
    def __get_all_by_tipo_resumen__(tipo):
        return Investigacion.query.filter(Investigacion.tipo_resumen == tipo).all()

    @staticmethod
    def __get_corpus_lemas__():
        columns = [Investigacion.id, Investigacion.corpus_lemas]
        return Investigacion.query.with_entities(*columns).all()

    @staticmethod
    def __get_corpus_lemas_autores__():
        columns = [Investigacion.id, Investigacion.corpus_lemas_autores]
        return Investigacion.query.with_entities(*columns).all()

    @classmethod
    def __get_columns__(cls):
        return [i for i in cls.__dict__.keys() if not i.startswith('_') or i == 'id']




class Calificaciones(db.Model):

    __tablename__ = 'calificaciones'

    id_calificacion = db.Column(db.Integer, primary_key=True, nullable=False)
    Usuarios_id_usuario = db.Column(db.Integer, ForeignKey(usuarios.id_usuario), nullable=False)
    usuarios=relationship("Usuarios", backref=backref("usuarios", uselist=False))
    opinion = db.Column(db.Text)
    calificacion = db.Column(db.Integer)


class Descargas(db.Model):

    __tablename__ = 'descargas'

    id_descarga = db.Column(db.Integer, primary_key=True, nullable=False)  
    Usuarios_id_usuario = db.Column(db.Integer, ForeignKey(usuarios.id_usuario), nullable=False)
    usuarios=relationship("Usuarios", backref=backref("usuarios", uselist=False))
    Investigaciones_id = db.Column(db.Integer, ForeignKey(investigaciones.id), nullable=False)
    investigaciones = relationship("Investigaciones", backref=backref("investigaciones", uselist=False))
    Busquedas_id_busqueda = db.Column(db.Integer, ForeignKey(busquedas.id_busqueda), nullable=False)
    busquedas=relationship("Busquedas", backref=backref("busquedas", uselist=False))
    #fecha_descarga = db.Column(db.Time)


class Busquedas(db.Model):

    __tablename__ = 'busquedas'

    id_busqueda = db.Column(db.Integer, primary_key=True, nullable=False)
    Usuarios_id_usuario = db.Column(db.Integer, ForeignKey(usuarios.id_usuario), nullable=False)
    usuarios=relationship("Usuarios", backref=backref("usuarios", uselist=False))
    #fecha_busqueda = db.Column(db.Time)
    busqueda = db.Column(db.Text)
    busqueda_preprocesada = db.Column(db.Text)


class Resultados(db.Model):
    
    __tablename__ = 'resultados'

    Busquedas_id_busqueda = db.Column(db.Integer, primary_key = True, ForeignKey(busquedas.id_busqueda), nullable=False)
    busquedas=relationship("Busquedas", backref=backref("busquedas", uselist=False))
    Investigaciones_id = db.Column(db.Array(db.Integer, primary_key = True, ForeignKey(investigaciones.id), nullable=False))
    investigaciones = relationship("Investigaciones", backref=backref("investigaciones", uselist=False))
