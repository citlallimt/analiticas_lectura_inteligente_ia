"""
Módulo de preprocesamiento del texto y del análisis lingüístico inicial.

Funciones:
- Lectura del documento.
- Limpieza del texto.
- Normalización.
- Preparación del documento para NLP.
"""

import warnings

import spacy
import textstat
from transformers import AutoTokenizer, pipeline


def load_text(file_path: str) -> str:
    """
    Lee un archivo de texto.

    Parámetros
    ----------
    file_path : str
        Ruta del archivo.

    Retorna
    -------
    str
        Texto del documento.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_spacy_model(language: str):
    """
    Carga automáticamente el modelo de spaCy.

    Parámetros
    ----------
    language : str
        Código del idioma ('es' o 'en').

    Retorna
    -------
    Language
        Modelo de spaCy.
    """

    if language == "es":
        model = "es_core_news_md"
    else:
        model = "en_core_web_md"

    return spacy.load(model)


def process_text(text: str, nlp):
    """
    Procesa el documento utilizando spaCy.
    """

    return nlp(text)


def get_stopwords(nlp):
    """
    Obtiene las stopwords del modelo spaCy.
    """

    return nlp.Defaults.stop_words


def calculate_text_metrics(text: str):
    """
    Calcula métricas básicas del documento.
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
    Calcula una aproximación de la complejidad léxica.
    """

    flesch = textstat.flesch_reading_ease(text)

    complexity = max(
        0,
        min(100, 100 - flesch)
    )

    return round(complexity, 2)


def analyze_sentiment(text):
    """
    Analiza el sentimiento general usando fragmentos controlados
    para evitar cierres inesperados por falta de memoria RAM.
    """
    if not text or not text.strip():
        return {'label': 'neutral', 'score': 0.0}

    try:
        from transformers import pipeline
        # Cargamos el pipeline de forma local
        classifier = pipeline("sentiment-analysis", model="pysentimiento/robertuito-sentiment-analysis")
        
        # En lugar de pasarle todo el texto pesado que asfixia la RAM,
        # le pasamos únicamente los primeros 400 caracteres (lo suficiente para el tono inicial)
        short_text = text[:400]
        result = classifier(short_text)
        
        if result:
            return {'label': result[0]['label'].lower(), 'score': round(float(result[0]['score']), 4)}
    except Exception:
        # Alternativa segura si el modelo falla o se queda sin memoria
        return {'label': 'neutral', 'score': 0.5000}
    
    return {'label': 'neutral', 'score': 0.5000}

    warnings.filterwarnings("ignore")

    model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=tokenizer,
        truncation=True,
        max_length=512
    )

    result = sentiment_pipeline(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"], 4)
    }
