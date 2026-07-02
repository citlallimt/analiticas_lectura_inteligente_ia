"""
Módulo encargado de extraer respuestas del documento
utilizando modelos Question Answering (QA).

Funciones:
- Carga del modelo RoBERTa QA.
- Extracción automática de respuestas.
"""

from transformers import pipeline
