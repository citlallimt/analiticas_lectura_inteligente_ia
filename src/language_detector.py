"""
Módulo encargado de detectar el idioma del documento
utilizando fast-langdetect.
"""

from fast_langdetect import detect_language

def detect_text_language(text):
    """
    Detecta el idioma de un texto.

    Parámetros:
        text (str): Texto a analizar.

    Retorna:
        str: Código del idioma detectado (es, en, etc.).
    """

    language = detect_language(text)

    return language.lower()
