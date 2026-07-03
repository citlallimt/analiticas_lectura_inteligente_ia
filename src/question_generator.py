"""
Módulo encargado de la generación automática de preguntas
a partir del contenido del documento utilizando el modelo T5.

Funciones:
- Carga del modelo T5.
- División del documento en fragmentos.
- Generación automática de preguntas.
- Eliminación de preguntas repetidas.
"""

from transformers import T5ForConditionalGeneration
from transformers import T5TokenizerFast
from thefuzz import fuzz
import re
import math


def load_question_generator():
    """
    Carga el modelo T5 utilizado para la generación automática
    de preguntas.

    Retorna
    -------
    tuple
        Modelo y tokenizer.
    """

    model_name = "valhalla/t5-base-qg-hl"

    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5TokenizerFast.from_pretrained(model_name)

    return model, tokenizer


def split_text(text: str, max_chunk_tokens: int = 450):
    """
    Divide un documento en fragmentos para facilitar
    la generación de preguntas.

    Parámetros
    ----------
    text : str
        Documento completo.

    max_chunk_tokens : int
        Número máximo aproximado de palabras por fragmento.

    Retorna
    -------
    list
        Lista de fragmentos.
    """

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


def remove_duplicate_questions(
    questions: list,
    similarity_threshold: int = 85
):
    """
    Elimina preguntas muy similares utilizando
    comparación difusa (TheFuzz).

    Parámetros
    ----------
    questions : list
        Lista de preguntas generadas.

    similarity_threshold : int
        Porcentaje máximo permitido de similitud.

    Retorna
    -------
    list
        Lista de preguntas sin duplicados.
    """

    filtered_questions = []

    for question in questions:

        is_duplicate = any(
            fuzz.ratio(
                question.lower(),
                existing.lower()
            ) > similarity_threshold
            for existing in filtered_questions
        )

        if not is_duplicate:
            filtered_questions.append(question)

    return filtered_questions


def generate_questions(text: str, target_questions: int = 5):
    """
    Genera preguntas automáticamente a partir del documento.

    Parámetros
    ----------
    text : str
        Texto del documento.

    target_questions : int
        Número aproximado de preguntas que se desea generar.

    Retorna
    -------
    list
        Lista de preguntas generadas.
    """

    model, tokenizer = load_question_generator()

    chunks = split_text(text)

    questions = []

    num_beams = 8
    num_beam_groups = 4

    questions_per_chunk = math.ceil(target_questions / len(chunks))

    num_return_sequences = min(
        math.ceil(questions_per_chunk * 2.5),
        num_beams
    )

    for chunk in chunks:

        input_text = "question generation: " + chunk

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
            max_length=128,
            num_beams=num_beams,
            num_beam_groups=num_beam_groups,
            diversity_penalty=0.5,
            early_stopping=True,
            no_repeat_ngram_size=2,
            num_return_sequences=num_return_sequences
        )

        generated = tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )

        questions.extend(generated)

    questions = remove_duplicate_questions(questions)

    return questions[:target_questions]
