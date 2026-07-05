"""
Módulo encargado de la generación automática de preguntas
con soporte multilingüe dinámico basado en el idioma detectado.

Funciones:
- Carga dinámica del modelo según el idioma.
- División del documento en fragmentos.
- Generación automática de preguntas.
- Eliminación de preguntas repetidas.
"""

from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from thefuzz import fuzz
import re
import math


def load_question_generator(lang: str = "es"):
    """
    Carga dinámicamente un modelo de generación de preguntas abierto
    basado en el idioma detectado, evitando errores de autenticación 401.

    Parámetros
    ----------
    lang : str
        Código del idioma detectado (ej. 'es', 'en').

    Retorna
    -------
    tuple
        Modelo y tokenizer correspondientes.
    """
    # Selección dinámica de modelos públicos y libres de candados 401
    if lang == "es":
        model_name = "mrm8488/bert2bert-spanish-question-generation"
    else:
        # Modelo estándar abierto para inglés y otros idiomas
        model_name = "valhalla/t5-base-qg-hl"

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return model, tokenizer


def split_text(text: str, max_chunk_tokens: int = 350):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(sentence.split())
        if current_tokens + sentence_tokens <= max_chunk_tokens:
            current_chunk += sentence + " "
            current_tokens += sentence_tokens
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_tokens = sentence_tokens

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def remove_duplicate_questions(questions: list, similarity_threshold: int = 75):
    filtered_questions = []
    for question in questions:
        if not question.endswith("?"):
            question += "?"
            
        is_duplicate = any(
            fuzz.ratio(question.lower(), existing.lower()) > similarity_threshold
            for existing in filtered_questions
        )
        if not is_duplicate:
            filtered_questions.append(question)
    return filtered_questions


def generate_questions(text: str, target_questions: int = 5, lang: str = "es"):
    """
    Genera preguntas automáticas adaptando el modelo según el idioma detectado.
    """
    # Pasamos el idioma detectado a la carga del modelo
    model, tokenizer = load_question_generator(lang=lang)
    chunks = split_text(text)

    if not chunks:
        return []

    questions = []
    num_beams = 4

    questions_per_chunk = math.ceil(target_questions / len(chunks))
    num_return_sequences = min(math.ceil(questions_per_chunk * 2), num_beams)

    for chunk in chunks:
        # Formato de entrada adaptado según el idioma
        if lang == "es":
            input_text = f"context: {chunk}"
        else:
            input_text = f"question generation: {chunk}"

        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding="longest"
        )

        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=64,
            num_beams=num_beams,
            early_stopping=True,
            no_repeat_ngram_size=3,
            num_return_sequences=num_return_sequences
        )

        generated = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        for question in generated:
            question = re.sub(r"^(pregunta|question):\s*", "", question, flags=re.IGNORECASE)
            question = question.strip()

            if len(question.split()) > 4:
                questions.append(question)

    questions = remove_duplicate_questions(questions)
    return questions[:target_questions]