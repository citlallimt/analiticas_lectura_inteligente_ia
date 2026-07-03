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


def get_stopwords(nlp):
    """
    Obtiene las palabras vacías (stopwords)
    del modelo de spaCy.

    Parámetros
    ----------
    nlp
        Modelo de spaCy.

    Retorna
    -------
    set
        Conjunto de stopwords.
    """

    return nlp.Defaults.stop_words


def calculate_text_metrics(text: str):
    """
    Calcula las métricas básicas del documento.

    Parámetros
    ----------
    text : str

    Retorna
    -------
    dict
        Número de palabras, oraciones y caracteres.
    """

    return {
        "word_count": textstat.lexicon_count(
            text,
            removepunct=True
        ),
        "sentence_count": textstat.sentence_count(text),
        "character_count": len(text)
    }


def calculate_lexical_complexity(text: str):
    """
    Calcula la complejidad léxica del documento.

    Parámetros
    ----------
    text : str

    Retorna
    -------
    float
        Complejidad entre 0 y 100.
    """

    flesch = textstat.flesch_reading_ease(text)

    complexity = max(
        0,
        min(100, 100 - flesch)
    )

    return round(complexity, 2)
