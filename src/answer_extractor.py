"""
Módulo encargado de la extracción automática de respuestas
utilizando modelos de Question Answering (QA) adaptados por idioma
mediante procesamiento directo de tensores por fragmentos.
"""

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import re


def load_qa_model(lang: str = "es"):
    """
    Carga dinámicamente el modelo y tokenizador de forma explícita
    según el idioma detectado, evitando el uso de pipelines con errores de registro.
    """
    if lang == "es":
        model_name = "deepset/xlm-roberta-base-squad2"
    else:
        model_name = "deepset/roberta-base-squad2"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    return model, tokenizer


def split_text_for_qa(text: str, max_chunk_tokens: int = 300):
    """
    Divide el texto en fragmentos más pequeños para que el modelo nativo
    pueda escanear y encontrar respuestas sin truncar la información.
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


def extract_answers(text: str, questions: list, lang: str = "es"):
    """
    Extrae las respuestas escaneando el documento por fragmentos utilizando tensores.
    """
    model, tokenizer = load_qa_model(lang=lang)
    chunks = split_text_for_qa(text)
    qa_pairs = []

    for index, question in enumerate(questions):
        best_answer = "No se encontró respuesta explícita en el documento."
        best_score = -9999.0

        # Escaneamos cada fragmento del texto para buscar la mejor respuesta a la pregunta
        for chunk in chunks:
            inputs = tokenizer(
                question, 
                chunk, 
                max_length=512, 
                truncation="only_second", 
                return_tensors="pt"
            )
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            start_logits = outputs.start_logits
            end_logits = outputs.end_logits
            
            # Calculamos el score de la respuesta candidata en este fragmento
            start_idx = torch.argmax(start_logits)
            end_idx = torch.argmax(end_logits) + 1
            
            # La suma de las probabilidades nos dice qué tan seguro está el modelo
            current_score = float(start_logits[0][start_idx] + end_logits[0][end_idx - 1])
            
            # Si es una mejor respuesta que la del fragmento anterior, la guardamos
            if current_score > best_score:
                answer_candidate = tokenizer.decode(inputs["input_ids"][0][start_idx:end_idx], skip_special_tokens=True).strip()
                
                # Descartar si el modelo seleccionó la propia pregunta o fragmentos vacíos
                if answer_candidate and len(answer_candidate) > 2 and answer_candidate.lower() not in question.lower():
                    best_score = current_score
                    best_answer = answer_candidate

        # Normalizamos un score para la visualización del reporte (escala 0-100 aproximada)
        final_score = round(max(0.0, min(100.0, (best_score + 10) * 5)), 2) if best_score != -9999.0 else 0.0

        qa_pairs.append({
            "id": index,
            "question": question,
            "answer": best_answer,
            "score": final_score
        })

    return qa_pairs