"""
Módulo encargado de evaluar la similitud semántica
entre las preguntas generadas y las respuestas obtenidas.

Funciones:
- Carga del modelo Sentence Transformer.
- Generación de embeddings.
- Cálculo de similitud coseno.
"""

from sentence_transformers import SentenceTransformer
from sentence_transformers import util


def load_similarity_model():
    """
    Carga el modelo utilizado para calcular
    la similitud semántica.

    Retorna
    -------
    SentenceTransformer
        Modelo de embeddings.
    """

    model = SentenceTransformer(
        "paraphrase-multilingual-mpnet-base-v2"
    )

    return model


def calculate_similarity(qa_pairs: list):
    """
    Calcula la similitud semántica entre cada
    pregunta y su respuesta.

    Parámetros
    ----------
    qa_pairs : list
        Lista de pares pregunta-respuesta.

    Retorna
    -------
    list
        Lista con la relevancia semántica agregada.
    """

    model = load_similarity_model()

    questions = [
        pair["question"]
        for pair in qa_pairs
    ]

    answers = [
        pair["answer"]
        for pair in qa_pairs
    ]

    question_embeddings = model.encode(
        questions,
        convert_to_tensor=True
    )

    answer_embeddings = model.encode(
        answers,
        convert_to_tensor=True
    )

    cosine_scores = util.pytorch_cos_sim(
        question_embeddings,
        answer_embeddings
    )

    results = []

    for index, pair in enumerate(qa_pairs):

        similarity = cosine_scores[index][index].item()

        relevance = round(
            ((similarity + 1) / 2) * 100,
            2
        )

        pair["semantic_similarity"] = relevance

        results.append(pair)

    return results
