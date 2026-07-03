"""
Archivo principal del proyecto.

Desde este módulo se ejecuta el flujo completo del sistema
Analíticas de Lectura Inteligente.
"""

from preprocessing import load_text
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

    # Ruta del documento de entrada
    input_file = "documento.txt"

    # 1. Lectura del documento
    text = load_text(input_file)

    # 2. Detección del idioma
    language = detect_text_language(text)

    print(f"Idioma detectado: {language}")

    # -----------------------------------------------------
    # Las siguientes etapas serán integradas conforme
    # se completen todos los módulos.
    # -----------------------------------------------------

    print("Procesamiento finalizado.")


if __name__ == "__main__":
    main()"""
Archivo principal del proyecto.

Desde este módulo se ejecuta el flujo completo del sistema
Analíticas de Lectura Inteligente.
"""

from preprocessing import load_text
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

    # Ruta del documento de entrada
    input_file = "documento.txt"

    # 1. Lectura del documento
    text = load_text(input_file)

    # 2. Detección del idioma
    language = detect_text_language(text)

    print(f"Idioma detectado: {language}")

    # -----------------------------------------------------
    # Las siguientes etapas serán integradas conforme
    # se completen todos los módulos.
    # -----------------------------------------------------

    print("Procesamiento finalizado.")


if __name__ == "__main__":
    main()
