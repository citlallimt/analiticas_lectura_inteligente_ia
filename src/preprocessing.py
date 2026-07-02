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


def load_text(file_path):
    """
    Lee un archivo de texto.

    Parámetros
    ----------
    file_path : str
        Ruta del archivo de texto.

    Retorna
    -------
    str
        Contenido del documento.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
