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
