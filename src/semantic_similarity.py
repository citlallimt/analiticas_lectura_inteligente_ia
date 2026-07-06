"""
Módulo encargado del cálculo de similitud semántica
utilizando distancias de Levenshtein (TheFuzz) para optimizar rendimiento.
"""

from thefuzz import fuzz


def calculate_similarity(qa_pairs: list):
    """
    Calcula la relevancia entre la pregunta y la respuesta usando distancias de Levenshtein.
    Evita congelamientos de red y ofrece scores realistas basados en coincidencia de texto.
    """
    if not qa_pairs:
        return []

    for pair in qa_pairs:
        question = pair.get("question", "")
        answer = pair.get("answer", "")

        # Si el modelo no encontró una respuesta válida, la relevancia es cero
        if "No se encontró" in answer or not answer:
            pair["relevance_score"] = 0.0
            continue

        try:
            # Usamos token_set_ratio que ignora el orden de las palabras y duplicados
            # Es perfecto para comparar una pregunta corta contra una frase de respuesta
            score = fuzz.token_set_ratio(question, answer)
            
            # Aseguramos un rango dinámico óptimo para el reporte de tesis
            pair["relevance_score"] = float(score)
            
        except Exception:
            pair["relevance_score"] = 0.0

    return qa_pairs