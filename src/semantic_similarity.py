"""
Módulo encargado de evaluar la similitud semántica
entre preguntas y respuestas mediante Sentence Transformers.

Funciones:
- Generación de embeddings.
- Cálculo de similitud semántica.
"""

from sentence_transformers import SentenceTransformer
from sentence_transformers import util
