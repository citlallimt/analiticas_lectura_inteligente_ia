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

    # =====================================================
    # 1. Lectura del documento
    # =====================================================

    input_file = "documento.txt"

    text = load_text(input_file)

    print("Documento cargado correctamente.")

    # =====================================================
    # 2. Detección del idioma
    # =====================================================

    language = detect_text_language(text)

    print(f"Idioma detectado: {language}")

    # =====================================================
    # 3. Procesamiento con spaCy
    # =====================================================

    nlp = load_spacy_model(language)

    doc = process_text(text, nlp)

    print("Documento procesado correctamente.")

    # =====================================================
    # 4. Métricas del documento
    # =====================================================

    metrics = calculate_text_metrics(text)

    print("\nMétricas del documento")

    print(metrics)

    # =====================================================
    # 5. Complejidad léxica
    # =====================================================

    complexity = calculate_lexical_complexity(text)

    print(f"\nComplejidad léxica: {complexity}")

    # =====================================================
    # 6. Análisis de sentimiento
    # =====================================================

    sentiment = analyze_sentiment(text)

    print("\nSentimiento del documento")

    print(sentiment)

    # =====================================================
    # 7. Análisis temático
    # =====================================================

    print("\n" + "=" * 60)
    print("ANÁLISIS TEMÁTICO")
    print("=" * 60)

    tokens = extract_tokens(doc)

    keywords = extract_keywords(
        text,
        language
    )

    print("\nPalabras clave:")

    for keyword in keywords:
        print(f"- {keyword}")

    dictionary, corpus, lda_model = build_lda_model(tokens)

    topics = get_topics(lda_model)

    print("\nTópicos detectados:")

    for topic, words in topics.items():
        print(f"{topic}: {words}")

    # =====================================================
    # Las siguientes etapas se integrarán después
    # =====================================================

    print("\nProcesamiento finalizado.")


if __name__ == "__main__":
    main()
