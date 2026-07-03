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
    """

    model_name = "PlanTL-GOB-ES/roberta-base-bne-sqac"

    qa_pipeline = pipeline(
        "question-answering",
        model=model_name,
        tokenizer=model_name
    )

    return qa_pipeline
