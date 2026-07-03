"""
Módulo encargado de la extracción automática de respuestas
utilizando modelos de Question Answering (QA).

Funciones:
- Carga del modelo RoBERTa QA.
- Extracción automática de respuestas.
"""

from transformers import pipeline


def load_qa_model():
    """
    Carga el modelo de Question Answering.

    Retorna
    -------
    pipeline
        Pipeline de Hugging Face para QA.
    """

    model_name = "PlanTL-GOB-ES/roberta-base-bne-sqac"

    qa_pipeline = pipeline(
        "question-answering",
        model=model_name,
        tokenizer=model_name
    )

    return qa_pipeline


def extract_answers(text: str, questions: list):
    """
    Extrae automáticamente las respuestas para
    una lista de preguntas.

    Parámetros
    ----------
    text : str
        Documento original.

    questions : list
        Lista de preguntas.

    Retorna
    -------
    list
        Lista de pares pregunta-respuesta.
    """

    qa_pipeline = load_qa_model()

    qa_pairs = []

    for index, question in enumerate(questions):

        result = qa_pipeline(
