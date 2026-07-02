"""
Módulo encargado de detectar el idioma del documento
utilizando fast-langdetect.
"""

from fast_langdetect import detect_language


def detect_text_language(text: str) -> str:
    """
    Detecta automáticamente el idioma de un texto.

    Parámetros
    ----------
    text : str
        Texto que será analizado.

    Retorna
    -------
    str
        Código del idioma detectado (por ejemplo: 'es', 'en').
    """

    try:
        language = detect_language(text)
        return language.lower()

    except Exception as error:
        raise RuntimeError(
            f"No fue posible detectar el idioma del texto: {error}"
        )
