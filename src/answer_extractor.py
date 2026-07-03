"""
Módulo encargado de extraer respuestas del documento
utilizando modelos Question Answering (QA).

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
        Pipeline de extracción de respuestas.
    """

    model_name = "PlanTL-GOB-ES/roberta-base-bne-sqac"

    qa_pipeline = pipeline(
        "question-answering",
        model=model_name,
        tokenizer=model_name
    )

    return qa_pipeline
