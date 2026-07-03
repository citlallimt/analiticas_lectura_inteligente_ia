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


def extract_tokens(doc):
    """
    Extrae los tokens más relevantes del documento
    para el análisis de tópicos.

    Parámetros
    ----------
    doc : spaCy Doc
        Documento procesado.

    Retorna
    -------
    list
        Lista de tokens normalizados.
    """

    allowed_pos = {"NOUN", "PROPN", "VERB", "ADJ"}

    tokens = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in allowed_pos
        and not token.is_stop
        and not token.is_punct
        and token.is_alpha
    ]

    return tokens
