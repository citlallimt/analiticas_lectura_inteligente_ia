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


def extract_keywords(text: str, language: str):
    """
    Extrae las palabras clave utilizando YAKE.

    Parámetros
    ----------
    text : str
        Texto del documento.

    language : str
        Idioma detectado.

    Retorna
    -------
    list
        Lista de palabras clave.
    """

    extractor = yake.KeywordExtractor(
        lan=language,
        n=1,
        dedupLim=0.9,
        top=15,
        features=None
    )

    keywords = extractor.extract_keywords(text)

    return [keyword for keyword, score in keywords][:10]


def build_lda_model(tokens: list, num_topics: int = 4):
    """
    Construye un modelo LDA.

    Parámetros
    ----------
    tokens : list
        Lista de tokens.

    num_topics : int
        Número de tópicos.

    Retorna
    -------
    tuple
        Diccionario, corpus y modelo LDA.
    """

    dictionary = Dictionary([tokens])

    dictionary.filter_extremes(
        no_below=1,
        no_above=1.0
    )

    corpus = [dictionary.doc2bow(tokens)]

    lda_model = LdaMulticore(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=15,
        iterations=100,
        random_state=100
    )

    return dictionary, corpus, lda_model


def get_topics(lda_model, num_topics: int = 4, num_words: int = 7):
    """
    Obtiene los tópicos principales generados por LDA.

    Parámetros
    ----------
    lda_model
        Modelo LDA entrenado.

    num_topics : int
        Número de tópicos.

    num_words : int
        Número de palabras por tópico.

    Retorna
    -------
    dict
        Diccionario con los tópicos principales.
    """

    topics = lda_model.show_topics(
        num_topics=num_topics,
        num_words=num_words,
        formatted=False
    )

    formatted_topics = {}

    for index, topic in topics:
        formatted_topics[f"topic_{index}"] = ", ".join(
            word for word, score in topic
        )

    return formatted_topics
