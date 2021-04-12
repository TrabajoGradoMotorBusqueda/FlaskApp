# Python Natives
import time

# Modulos Procesamiento de Texto
from .corpus import construccion_corpus
from .lemas import lematizar_corpus
from .estructura_datos import estructura_dataset, leer_resumenes
from .almacenar_datos import almacenar_resumen, construir_corpus, almacenar_vocabulario
from main import BASE_DIR


def iniciar_fixmi():
    print('Entramos')
    start = time.time()
    # # Cargar Resumenes
    # resumenes_docentes, resumenes_estudiantes = leer_resumenes()
    # # Estructurar Resumenes
    # docentes = estructura_dataset(resumenes_docentes)
    # estudiantes = estructura_dataset(resumenes_estudiantes)
    # # Eliminar Resumenes Originales
    # del resumenes_docentes, resumenes_estudiantes
    # # Almacenar Datos
    # almacenar_resumen(docentes, 'docentes')  # Almacenar Datos Docentes
    # almacenar_resumen(estudiantes, 'estudiantes')  # Almacenar Datos Estudiantes
    # # Almacenar csv
    # docentes.to_csv(BASE_DIR / 'FILES/resumenes/Resumenes_Docentes.csv')
    # docentes.to_csv(BASE_DIR / 'FILES/resumenes/Resumenes_Estudiantes.csv')
    # # Eliminar Resumenes Transformados
    # del docentes, estudiantes
    # # Construccion de Corpus y Vocabulario
    # construir_corpus()
    #
    # # Seguimos con la Ontologia
    # from ontologia import instancias_investigaciones as ontologia_instanciar
    # ontologia_instanciar.iniciar_instancia_ontologia()

    # Entrenar d2v
    from doc2vec import entrenar_d2v
    entrenar_d2v()

    print('fixmi concluido')
    end = time.time()
    minutes, seconds = divmod(end - start, 60)
    print(f'Minutos: {minutes} - Segundos: {seconds}')
