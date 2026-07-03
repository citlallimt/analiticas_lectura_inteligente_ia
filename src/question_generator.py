"""
Módulo encargado de la generación automática de preguntas
a partir del contenido del documento utilizando el modelo T5.

Funciones:
- Carga del modelo T5.
- Generación automática de preguntas.
- Eliminación de preguntas repetidas.
"""

from transformers import T5ForConditionalGeneration
from transformers import T5TokenizerFast
from thefuzz import fuzz
import re
import math


def load_question_generator():
    """
    Carga el modelo T5 utilizado para la generación automática
    de preguntas.

    Retorna
    -------
    tuple
        Modelo y tokenizer.
    """

    model_name = "valhalla/t5-base-qg-hl"

    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5TokenizerFast.from_pretrained(model_name)

    return model, tokenizer


def split_text(text: str, max_chunk_tokens: int = 450):
    """
    Divide un documento en fragmentos para facilitar
    la generación de preguntas.

    Parámetros
    ----------
    text : str
        Documento completo.

    max_chunk_tokens : int
        Número máximo aproximado de palabras por fragmento.

    Retorna
    -------
    list
        Lista de fragmentos.
    """

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:

        sentence_tokens = len(sentence.split())

        if current_tokens + sentence_tokens <= max_chunk_tokens:

            current_chunk += sentence + " "
            current_tokens += sentence_tokens

        else:

            chunks.append(current_chunk.strip())

            current_chunk = sentence + " "
            current_tokens = sentence_tokens

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
