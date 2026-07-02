"""
Módulo encargado del análisis temático del documento.

Funciones:
- Extracción de palabras clave.
- Modelado de tópicos mediante LDA.
- Identificación de los temas principales.
"""

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
import yake
