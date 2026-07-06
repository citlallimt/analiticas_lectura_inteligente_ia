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
from summarizer import generate_summary


def run_pipeline(input_file):

    print("=" * 80)
    print("ANALÍTICAS DE LECTURA INTELIGENTE")
    print("=" * 80)

    # =====================================================
    # 1. Lectura del Documento
    # =====================================================
    text = load_text(input_file)
    print("Documento cargado correctamente.")

    # =====================================================
    # 2. Detección de Idioma
    # =====================================================
    language = detect_text_language(text)
    print(f"Idioma detectado: {language}")

    # =====================================================
    # 3. Resumen Automático (Nueva Fase 1)
    # =====================================================
    print("\n" + "=" * 80)
    print("RESUMEN AUTOMÁTICO DEL DOCUMENTO")
    print("=" * 80)

    try:
        summary = generate_summary(text, language=language)
        print(summary)
    except Exception as e:
        summary = "No fue posible generar el resumen de forma automática."
        print(summary)
        print(f"Detalle: {e}")
        
    print("=" * 80)

    # =====================================================
    # 4. Procesamiento spaCy
    # =====================================================
    nlp = load_spacy_model(language)
    doc = process_text(text, nlp)
    print("\nDocumento procesado correctamente con spaCy.")

    # =====================================================
    # 5. Métricas de Lectura
    # =====================================================
    metrics = calculate_text_metrics(text)
    print("\nMÉTRICAS DEL DOCUMENTO")
    print(metrics)

    # =====================================================
    # 6. Complejidad Léxica
    # =====================================================
    complexity = calculate_lexical_complexity(text)
    print(f"\nComplejidad léxica: {complexity}")

    # =====================================================
    # 7. Análisis de Sentimiento
    # =====================================================
    sentiment = analyze_sentiment(text)
    print("\nANÁLISIS DE SENTIMIENTO")
    print(sentiment)

    # =====================================================
    # 8. Análisis Temático y Tópicos
    # =====================================================
    print("\n" + "=" * 80)
    print("ANÁLISIS TEMÁTICO")
    print("=" * 80)

    tokens = extract_tokens(doc)
    keywords = extract_keywords(text, language)

    print("\nPalabras clave:")
    for keyword in keywords:
        print("-", keyword)

    dictionary, corpus, lda_model = build_lda_model(tokens)
    topics = get_topics(lda_model)

    print("\Tópicos detectados:")
    for topic, words in topics.items():
        print(f"{topic}: {words}")

    # =====================================================
    # 9. Generación Automática de Preguntas
    # =====================================================
    print("\n" + "=" * 80)
    print("GENERACIÓN DE PREGUNTAS")
    print("=" * 80)

    # CAMBIAMOS 'text' POR 'summary' PARA QUE PREGUNTE SOBRE LAS IDEAS PRINCIPALES
    questions = generate_questions(
        summary,  # <-- Aquí cambiamos text por summary
        target_questions=5,
        lang=language
    )

    for i, q in enumerate(questions, start=1):
        print(f"{i}. {q}")

    # =====================================================
    # 10. Extracción Nativa de Respuestas
    # =====================================================
    print("\n" + "=" * 80)
    print("EXTRACCIÓN DE RESPUESTAS")
    print("=" * 80)

    qa_pairs = extract_answers(
        text,
        questions,
        lang=language
    )

    # =====================================================
    # 11. Cálculo de Similitud Semántica (TheFuzz)
    # =====================================================
    qa_pairs = calculate_similarity(qa_pairs)

    # Impresión estructurada de los pares Q&A finales evaluados
    for i, pair in enumerate(qa_pairs, start=1):
        print(f"\nPregunta {i}:")
        print(pair["question"])
        print("Respuesta:")
        print(pair["answer"])
        print(f"Score Confianza QA: {pair.get('score', 0.0)}")
        print(f"Relevancia Semántica: {pair.get('relevance_score', 0.0)}%")

    # =====================================================
    # 12. Guardado del Reporte de Analíticas
    # =====================================================
    save_report(
        input_file=input_file,
        metrics=metrics,
        complexity=complexity,
        sentiment=sentiment,
        keywords=keywords,
        topics=topics,
        qa_pairs=qa_pairs
    )

    print("\nProcesamiento finalizado exitosamente. Reporte generado.")

    # =====================================================
    # RETORNO DE RESULTADOS PARA LA INTERFAZ GRÁFICA (GUI)
    # =====================================================
    return {
        "text": text,
        "language": language,
        "summary": summary,
        "metrics": metrics,
        "complexity": complexity,
        "sentiment": sentiment,
        "keywords": keywords,
        "topics": topics,
        "questions": questions
    }


def main():
    # Ejecuta el análisis sobre tu archivo de texto por defecto
    run_pipeline("documento.txt")


if __name__ == "__main__":
    main()