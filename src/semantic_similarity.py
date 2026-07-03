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
  
