"""
Módulo de preprocesamiento del texto y del análisis lingüístico inicial.

Funciones:
- Lectura del documento.
- Limpieza del texto.
- Normalización.
- Preparación del documento para NLP.
"""

import spacy
import textstat
from transformers import pipeline, AutoTokenizer
import warnings

from language_detector import detect_text_language


def load_text(file_path: str) -> str:
    """
    Lee un archivo de texto.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_spacy_model(language: str):
    """
    Carga automáticamente el modelo de spaCy
    correspondiente al idioma detectado.

    Parámetros
    ----------
    language : str
        Código del idioma ('es' o 'en').

    Retorna
    -------
    Language
        Modelo de spaCy cargado.
    """

    if language == "es":
        model = "es_core_news_md"
    else:
        model = "en_core_web_md"

    return spacy.load(model)


def process_text(text: str, nlp):
    """
    Procesa el documento utilizando spaCy.

    Parámetros
    ----------
    text : str
        Texto original.

    nlp :
        Modelo de spaCy cargado.

    Retorna
    -------
    Doc
        Documento procesado.
    """

    return nlp(text)
