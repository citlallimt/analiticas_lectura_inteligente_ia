"""
Módulo encargado del análisis de sentimiento del documento.

Utiliza modelos preentrenados de Hugging Face para identificar
la polaridad del texto y estimar la percepción general
del contenido analizado.

Funciones:
- Carga del modelo de análisis de sentimiento.
- Clasificación del sentimiento del documento.
"""

from transformers import pipeline
from transformers import AutoTokenizer
