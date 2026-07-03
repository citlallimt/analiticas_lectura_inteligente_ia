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
    """

    model = SentenceTransformer(
        "paraphrase-multilingual-mpnet-base-v2"
    )

    return model


def calculate_similarity(qa_pairs: list):
    """
    Calcula la similitud semántica entre
    cada pregunta y su respuesta.

    Parámetros
    ----------
    qa_pairs : list
        Lista de pares pregunta-respuesta.

    Retorna
    -------
    list
        Lista actualizada con la relevancia semántica.
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

    similarity_matrix = util.pytorch_cos_sim(
        question_embeddings,
        answer_embeddings
    )

    results = []

    for i, pair in enumerate(qa_pairs):

        similarity = similarity_matrix[i][i].item()

        relevance = max(
            0,
            min(
                100,
                ((similarity + 1) / 2) * 100
            )
        )

        pair["relevance_score"] = round(
            relevance,
            2
        )

        results.append(pair)

    return results
