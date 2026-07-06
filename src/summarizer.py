"""
summarizer.py

Generación automática de resúmenes ejecutivos optimizados
para Analíticas de Lectura Inteligente.
"""

import re

def generate_summary(text: str, language: str = "es", max_sentences: int = 3):
    """
    Genera un resumen ejecutivo del documento seleccionando las oraciones
    más representativas según la densidad de palabras clave, evitando sobrecargar la RAM.
    """
    if not text or not text.strip():
        return "No existe contenido para resumir."

    try:
        # Dividimos el texto en oraciones de forma limpia
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        if len(sentences) <= max_sentences:
            return text.strip()

        # Almacenamos palabras significativas ignorando conectores cortos
        words = [w.lower() for w in text.split() if len(w) > 4]
        word_frequencies = {}
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

        # Puntuamos cada oración según la importancia de sus palabras
        sentence_scores = {}
        for sentence in sentences:
            sentence_scores[sentence] = 0
            for word in sentence.split():
                if word.lower() in word_frequencies:
                    sentence_scores[sentence] += word_frequencies[word.lower()]

        # Seleccionamos las oraciones con los puntajes más altos en el orden original
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
        summary = " ".join([s for s in sentences if s in top_sentences])

        return summary.strip()

    except Exception as e:
        return f"No fue posible generar el resumen de forma automática.\nDetalle: {e}"