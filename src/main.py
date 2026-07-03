"""
Archivo principal del proyecto.

Desde este módulo se ejecuta el flujo completo del sistema
Analíticas de Lectura Inteligente.
"""

from preprocessing import (
    load_text,
    load_spacy_model,
    process_text,
    calculate_text_metrics,
    calculate_lexical_complexity,
    analyze_sentiment
)

from language_detector import detect_text_language

from topic_model import (
    extract_tokens,
    extract_keywords,
    build_lda_model,
    get_topics
)

from question_generator import generate_questions
from answer_extractor import extract_answers
from semantic_similarity import calculate_similarity
from report_generator import save_report


def main():
    """
    Ejecuta el flujo principal del sistema.
    """

    print("=" * 60)
    print("ANALÍTICAS DE LECTURA INTELIGENTE")
    print("=" * 60)

    # Ruta del documento
    input_file = "documento.txt"

    # -------------------------------------------------
    # 1. Leer documento
    # -------------------------------------------------

    text = load_text(input_file)

    # -------------------------------------------------
    # 2. Detectar idioma
    # -------------------------------------------------

    language = detect_text_language(text)

    print(f"Idioma detectado: {language}")

    # -------------------------------------------------
    # 3. Cargar modelo spaCy
    # -------------------------------------------------

    nlp = load_spacy_model(language)

    # -------------------------------------------------
    # 4. Procesar documento
    # -------------------------------------------------

    doc = process_text(text, nlp)

    print("Documento procesado correctamente.")

    # -------------------------------------------------
    # 5. Métricas
    # -------------------------------------------------

    metrics = calculate_text_metrics(text)

    print("\nMétricas del documento:")
    print(metrics)

    # -------------------------------------------------
    # 6. Complejidad léxica
    # -------------------------------------------------

    complexity = calculate_lexical_complexity(text)

    print(f"\nComplejidad léxica: {complexity}")

    # -------------------------------------------------
    # 7. Sentimiento
    # -------------------------------------------------

    sentiment = analyze_sentiment(text)

    print("\nAnálisis de sentimiento:")
    print(sentiment)

    # -------------------------------------------------
    # Las siguientes fases se irán integrando
    # -------------------------------------------------

    print("\nProcesamiento finalizado.")


if __name__ == "__main__":
    main()
