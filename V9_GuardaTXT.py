# -*- coding: utf-8 -*-
"""
Script Unificado para Análisis de Texto, Generación de Preguntas y Respuestas
Fases:
1. Análisis de Texto (Idioma, Tema, Palabras Clave, Complejidad, Longitud, Sentimiento)
2. Generación de Preguntas Guiada
3. Extracción de Respuestas
4. (Opcional) Evaluación de Relevancia Pregunta-Respuesta
5. (Opcional) Guardado de Resultados en .txt
"""

# --- Importaciones Necesarias ---
import spacy
from fast_langdetect import detect_language
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
import yake
import textstat
# Se elimina AutoModelForSeq2SeqLM que era para la reformulación
from transformers import pipeline, T5ForConditionalGeneration, T5TokenizerFast, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
from thefuzz import fuzz
import re
import os
import math
import warnings
# Importaciones para el selector de archivos y manejo de rutas (se mantiene)
from tkinter import Tk, filedialog

# Ignorar advertencias
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module='fast_langdetect')
warnings.filterwarnings("ignore", category=FutureWarning, module='transformers.pipelines.Youtubeing')

# --- Configuración Inicial ---
INPUT_TEXT_FILE_PATH = "La_Revolución_Háptica_IAEV.txt"
if not os.path.exists(INPUT_TEXT_FILE_PATH):
    print(f"Error Crítico: El archivo de entrada '{INPUT_TEXT_FILE_PATH}' no fue encontrado.")
    exit()

# --- Funciones Fase 1: Análisis de Texto (SIN CAMBIOS) ---
def process_phase1(file_path):
    print("--- Iniciando Fase 1: Análisis de Texto ---")
    results = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        if not text.strip():
            print(f"Error: El archivo '{file_path}' está vacío.")
            return None
        results['original_text'] = text
        print(f"Texto leído desde: {file_path}")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

    try:
        lang_code_original = detect_language(text)
        lang_code = lang_code_original.lower()
        results['language'] = lang_code
        print(f"Idioma detectado: {lang_code_original} (usando '{lang_code}' para procesamiento)")
        if lang_code not in ['en', 'es']:
            print(f"Advertencia: Idioma detectado '{lang_code_original}' no soportado. Análisis completo no disponible.")
            results['length'] = {'word_count': len(text.split())}
            return results
    except Exception as e:
        print(f"Error en detección de idioma: {e}.")
        return None

    try:
        model_name_spacy = "es_core_news_md" if lang_code == 'es' else "en_core_web_md"
        print(f"Cargando modelo spaCy: {model_name_spacy}...")
        nlp = spacy.load(model_name_spacy)
        spacy_stopwords = nlp.Defaults.stop_words
        print("Procesando texto con spaCy...")
        doc = nlp(text)
        results['spacy_doc'] = doc
        print(f"Texto procesado con spaCy usando modelo: {model_name_spacy}")
        allowed_pos = {'NOUN', 'PROPN', 'VERB', 'ADJ'}
        processed_tokens = [
            token.lemma_.lower() for token in doc
            if token.pos_ in allowed_pos and not token.is_stop and not token.is_punct and token.is_alpha
        ]
        results['processed_tokens_for_lda'] = processed_tokens
        print(f"Tokens procesados para LDA: {len(processed_tokens)}")
    except Exception as e:
        print(f"Error en procesamiento con spaCy: {e}")
        return None

    num_topics_lda = 4
    if 'processed_tokens_for_lda' in results and len(results['processed_tokens_for_lda']) > num_topics_lda:
        try:
            print("Iniciando modelado de tópicos LDA...")
            local_processed_tokens = results['processed_tokens_for_lda']
            
            if not local_processed_tokens:
                print("    LDA: processed_tokens_for_lda está vacía. Omitiendo LDA.")
                results['topics'] = "No aplicable (no hay tokens para LDA)"
            else:
                dictionary = Dictionary([local_processed_tokens])
                dictionary.filter_extremes(no_below=1, no_above=1.0) 
                corpus = [dictionary.doc2bow(local_processed_tokens)]

                if len(dictionary) > 0 and corpus and any(corpus[0]): 
                    print(f"Entrenando modelo LDA con {num_topics_lda} tópicos y {len(dictionary)} términos en diccionario...")
                    lda_model = LdaMulticore(
                        corpus=corpus, id2word=dictionary, num_topics=num_topics_lda,
                        workers=max(1, os.cpu_count() - 1), passes=15, iterations=100, random_state=100
                    )
                    results['lda_model'] = lda_model
                    topics_raw = lda_model.show_topics(num_topics=num_topics_lda, num_words=7, formatted=False)
                    topics_formatted = {f"topic_{idx}": ", ".join([word for word, prop in topic]) for idx, topic in topics_raw}
                    results['topics'] = {
                        'main_topic': topics_formatted.get('topic_0', 'N/A'),
                        'subtopic_1': topics_formatted.get('topic_1', 'N/A'),
                        'subtopic_2': topics_formatted.get('topic_2', 'N/A'),
                        'subtopic_3': topics_formatted.get('topic_3', 'N/A')
                    }
                    print("Modelado de tópicos LDA completado.")
                else:
                    print("Diccionario LDA o corpus vacío/inválido después de filtrar, omitiendo modelado de tópicos.")
                    results['topics'] = "No aplicable (diccionario/corpus vacío)"
        except Exception as e:
            print(f"Error en modelado de tópicos LDA: {e}")
            results['topics'] = f"Error: {e}"
    else:
        print("Texto demasiado corto o sin tokens válidos suficientes para modelado de tópicos LDA.")
        results['topics'] = "No aplicable (texto corto o tokens insuficientes)"

    try:
        print("Extrayendo palabras clave con YAKE...")
        kw_extractor = yake.KeywordExtractor(lan=lang_code, n=1, dedupLim=0.9, top=15, features=None)
        keywords_scored = kw_extractor.extract_keywords(text)
        keywords = [kw for kw, score in keywords_scored if kw.lower() not in spacy_stopwords][:10]
        results['keywords'] = keywords
        print(f"Palabras clave extraídas (YAKE, Top 10 no-stopwords): {keywords}")
    except Exception as e:
        print(f"Error en extracción de palabras clave (YAKE): {e}")
        results['keywords'] = f"Error: {e}"

    try:
        print("Calculando métricas de texto...")
        textstat.set_lang(lang_code)
        word_count = textstat.lexicon_count(text, removepunct=True)
        sentence_count = textstat.sentence_count(text)
        results['length'] = {'word_count': word_count, 'sentence_count': sentence_count, 'character_count': len(text)}
        print(f"Métricas de longitud: Palabras={word_count}, Oraciones={sentence_count}")
        flesch_score = textstat.flesch_reading_ease(text)
        complexity_score = max(0.0, min(100.0, 100.0 - flesch_score))
        results['lexical_complexity'] = round(complexity_score, 2)
        print(f"Complejidad léxica (0-100, mayor=más complejo): {results['lexical_complexity']:.2f} (Flesch original: {flesch_score:.2f})")
    except Exception as e:
        print(f"Error calculando métricas de texto (textstat): {e}")
        if 'length' not in results: results['length'] = {}
        results['lexical_complexity'] = f"Error: {e}"
        
    try:
        print("Iniciando análisis de sentimiento...")
        sentiment_model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        tokenizer_for_sentiment = AutoTokenizer.from_pretrained(sentiment_model_name)
        effective_max_length = getattr(tokenizer_for_sentiment, 'model_max_length', 512)
        if effective_max_length > 512 or effective_max_length <=0 :
                effective_max_length = 512

        sentiment_pipeline_instance = pipeline(
            "sentiment-analysis", model=sentiment_model_name, tokenizer=tokenizer_for_sentiment,
            truncation=True, max_length=effective_max_length, padding="max_length", device="cpu"
        )
        sentiment_result_list = sentiment_pipeline_instance(text)

        if sentiment_result_list and isinstance(sentiment_result_list, list):
            sentiment_data = sentiment_result_list[0].copy()
            label_map = {'LABEL_0': 'Negativo', 'LABEL_1': 'Neutral', 'LABEL_2': 'Positivo',
                         'negative': 'Negativo', 'neutral': 'Neutral', 'positive': 'Positivo'}
            sentiment_data['label'] = label_map.get(sentiment_data['label'].lower(), sentiment_data['label'])
            results['sentiment'] = sentiment_data
            print(f"Análisis de sentimiento: {results['sentiment']}")
        else:
            results['sentiment'] = "No se pudo obtener resultado de sentimiento."
    except Exception as e:
        print(f"Error en análisis de sentimiento: {e}")
        results['sentiment'] = f"Error: {e}"

    print("\n--- Resumen Resultados Fase 1 ---")
    print(f"Archivo: {file_path}")
    print(f"Idioma: {results.get('language', 'N/A')}")
    if results.get('language') in ['en', 'es']:
        length_res = results.get('length', {})
        if isinstance(length_res, dict): print(f"Longitud: Palabras={length_res.get('word_count', 'N/A')}, Oraciones={length_res.get('sentence_count', 'N/A')}")
        else: print(f"Longitud: {length_res}")
        comp_res = results.get('lexical_complexity', 'N/A')
        if isinstance(comp_res, (float, int)): print(f"Complejidad Léxica (0-100): {comp_res:.2f}")
        else: print(f"Complejidad Léxica (0-100): {comp_res}")
        sentiment_res = results.get('sentiment', {})
        if isinstance(sentiment_res, dict): print(f"Sentimiento: Label='{sentiment_res.get('label', 'N/A')}', Score={sentiment_res.get('score', -1.0):.4f}")
        else: print(f"Sentimiento: {sentiment_res}")
        keywords_res = results.get('keywords', 'N/A')
        if isinstance(keywords_res, list): print(f"Palabras Clave (Top 10): {', '.join(keywords_res) if keywords_res else 'Ninguna'}")
        else: print(f"Palabras Clave (Top 10): {keywords_res}")
        topics_res = results.get('topics', {})
        if isinstance(topics_res, dict):
            print("Tópicos (LDA):")
            for k, v in topics_res.items(): print(f"  - {k.replace('_', ' ').capitalize()}: {v}")
        else: print(f"Tópicos (LDA): {topics_res}")
    else: print("Análisis detallado omitido (idioma no soportado).")
    print("--- Fin Fase 1 ---")
    return results

# --- La función de reformulación de preguntas ha sido eliminada. ---

def process_phase2(phase1_results):
    # El título vuelve a su estado original
    print("\n--- Iniciando Fase 2: Generación de Preguntas ---")
    if not phase1_results or 'original_text' not in phase1_results or phase1_results.get('language') not in ['en', 'es']:
        print("Error: Resultados de Fase 1 no disponibles, incompletos o idioma no soportado.")
        return phase1_results if phase1_results else None

    text = phase1_results['original_text']
    doc_language = phase1_results.get('language', 'es')
    word_count = phase1_results.get('length', {}).get('word_count', 0)
    if not isinstance(word_count, int): word_count = len(text.split())

    phase1_results['phase2_results'] = {'generated_questions': [], 'target_num_questions': 0}
    results_f2 = phase1_results['phase2_results']
    target_num_questions = max(3, min(10, math.floor(word_count / 150) + 3)) if word_count > 50 else 0
    results_f2['target_num_questions'] = target_num_questions

    if target_num_questions == 0:
        print("Texto demasiado corto. Omitiendo generación de preguntas.")
        return phase1_results
    print(f"Objetivo de preguntas a generar: {target_num_questions}")

    try:
        print("Cargando modelo de generación de preguntas (T5)...")
        qg_model_name = "valhalla/t5-base-qg-hl"
        qg_model = T5ForConditionalGeneration.from_pretrained(qg_model_name)
        qg_tokenizer = T5TokenizerFast.from_pretrained(qg_model_name)
        print(f"Modelo QG cargado: {qg_model_name}")

        sentences = re.split(r'(?<=[.!?])\s+', text)
        max_chunk_tokens, chunks, current_chunk, current_tokens = 450, [], "", 0
        for sentence in sentences:
            sentence_tokens = len(sentence.split())
            if current_tokens + sentence_tokens <= max_chunk_tokens:
                current_chunk += sentence + " "; current_tokens += sentence_tokens
            else:
                if current_chunk: chunks.append(current_chunk.strip())
                current_chunk = sentence + " "; current_tokens = sentence_tokens
        if current_chunk: chunks.append(current_chunk.strip())
        if not chunks: chunks = [text]
        num_chunks = len(chunks)

        questions_per_chunk_target = math.ceil(target_num_questions / num_chunks) if num_chunks > 0 else target_num_questions
        
        num_beams_qg = 8 
        num_beam_groups_qg = 4 
        
        desired_returns_per_chunk = math.ceil(questions_per_chunk_target * 2.5)
        num_return_sequences_qg = min(desired_returns_per_chunk, num_beams_qg)
        num_return_sequences_qg = max(num_return_sequences_qg, num_beam_groups_qg)
        if num_beam_groups_qg > 1 and num_return_sequences_qg > num_beam_groups_qg and num_return_sequences_qg % num_beam_groups_qg != 0:
            num_return_sequences_qg = (num_return_sequences_qg // num_beam_groups_qg) * num_beam_groups_qg
            if num_return_sequences_qg == 0: 
                num_return_sequences_qg = num_beam_groups_qg
        
        print(f"  Parámetros QG por chunk: num_beams={num_beams_qg}, num_beam_groups={num_beam_groups_qg}, num_return_sequences={num_return_sequences_qg}")

        all_generated_questions_set = set()
        print(f"Procesando texto en {num_chunks} fragmento(s) para generar ~{target_num_questions} preguntas finales...")
        for i, chunk_text in enumerate(chunks):
            print(f"  Generando preguntas candidatas para fragmento {i+1}/{num_chunks}...")
            input_text_qg = "question generation: " + chunk_text
            inputs_qg = qg_tokenizer(input_text_qg, return_tensors="pt", max_length=512, truncation=True, padding="longest")
            
            output_sequences = qg_model.generate(
                input_ids=inputs_qg['input_ids'], attention_mask=inputs_qg['attention_mask'],
                max_length=128, 
                num_beams=num_beams_qg,
                num_beam_groups=num_beam_groups_qg, 
                diversity_penalty=0.5, 
                early_stopping=True, no_repeat_ngram_size=2,
                num_return_sequences=num_return_sequences_qg,
                length_penalty=1.0 
            )
            generated_for_chunk = qg_tokenizer.batch_decode(output_sequences, skip_special_tokens=True)

            for q in generated_for_chunk:
                q_cleaned = re.sub(r'^(question|pregunta):\s*', '', q, flags=re.IGNORECASE).strip()
                if len(q_cleaned.split()) > 3 and q_cleaned.endswith('?'):
                    try:
                        q_lang = detect_language(q_cleaned).lower()
                        if q_lang == doc_language:
                            all_generated_questions_set.add(q_cleaned)
                    except Exception as lang_err:
                        print(f"    Advertencia: Falló la detección de idioma para '{q_cleaned[:60]}...' ({lang_err}). Pregunta descartada.")
        
        candidate_questions_list = sorted(list(all_generated_questions_set))
        final_selected_questions = []
        SIMILARITY_THRESHOLD = 85 
        if candidate_questions_list:
            final_selected_questions.append(candidate_questions_list[0])
            for q_new in candidate_questions_list[1:]:
                is_too_similar = any(fuzz.ratio(q_new.lower(), q_selected.lower()) > SIMILARITY_THRESHOLD for q_selected in final_selected_questions)
                if not is_too_similar:
                    final_selected_questions.append(q_new)
        
        # --- LÓGICA DE REFORMULACIÓN ELIMINADA ---
        # Ahora simplemente se toman las preguntas filtradas hasta alcanzar el objetivo.
        results_f2['generated_questions'] = final_selected_questions[:target_num_questions]
        
        # El mensaje de impresión se ajusta para no mencionar la reformulación
        num_generated = len(results_f2['generated_questions'])
        print(f"Preguntas generadas ({num_generated} de {target_num_questions} objetivo final):")
        if num_generated == 0: print("  No se pudieron generar preguntas válidas.")
        else:
            for i_q, q_text in enumerate(results_f2['generated_questions']): print(f"  {i_q+1}. {q_text}")
    except Exception as e:
        print(f"Error en generación de preguntas (T5): {e}")
        results_f2['generated_questions'] = f"Error: {e}"

    print("\n--- Resumen Resultados Fase 2 ---")
    print(f"Número objetivo de preguntas: {results_f2.get('target_num_questions', 'N/A')}")
    generated_q_list = results_f2.get('generated_questions')
    if isinstance(generated_q_list, list):
        print(f"Número de preguntas generadas: {len(generated_q_list)}")
    else:
        print(f"Preguntas generadas: {generated_q_list}")
    print("--- Fin Fase 2 ---")
    return phase1_results

# --- Fase 3 (Extracción de Respuestas): SIN CAMBIOS ---
def process_phase3(phase1_and_2_results):
    print("\n--- Iniciando Fase 3: Extracción de Respuestas ---")
    if not phase1_and_2_results or \
       'original_text' not in phase1_and_2_results or \
       'phase2_results' not in phase1_and_2_results or \
       'generated_questions' not in phase1_and_2_results['phase2_results']:
        print("Error: Resultados de Fases 1 o 2 no disponibles o incompletos.")
        return phase1_and_2_results

    text = phase1_and_2_results['original_text']
    questions = phase1_and_2_results['phase2_results']['generated_questions']

    phase1_and_2_results['phase3_results'] = {'qa_pairs': []}
    results_f3 = phase1_and_2_results['phase3_results']

    if not isinstance(questions, list):
        print("Error: Las preguntas generadas no están en el formato esperado (lista).")
        if isinstance(questions, str) and questions.startswith("Error"):
            print(f"  Detalle del error previo en Fase 2: {questions}")
        print("--- Fin Fase 3 (Abortada) ---")
        return phase1_and_2_results

    if not questions:
        print("No hay preguntas generadas para extraer respuestas.")
        print("--- Fin Fase 3 ---")
        return phase1_and_2_results

    try:
        print("Cargando modelo de Question Answering...")
        qa_model_name = "PlanTL-GOB-ES/roberta-base-bne-sqac"
        print(f"Usando modelo QA: {qa_model_name}")
        qa_pipeline_instance = pipeline('question-answering', model=qa_model_name, tokenizer=qa_model_name, device="cpu")
        print("Pipeline QA cargado.")

        print(f"Extrayendo respuestas para {len(questions)} preguntas...")
        for i, question_text in enumerate(questions):
            try:
                qa_input = {'question': question_text, 'context': text}
                answer_result = qa_pipeline_instance(qa_input)
                answer_text = answer_result.get('answer', '').strip()
                answer_score = answer_result.get('score', 0.0)
                
                if answer_text:
                    results_f3['qa_pairs'].append({
                        'id': i, 'question': question_text, 'answer': answer_text,
                        'score': round(answer_score, 4),
                    })
                else:
                    results_f3['qa_pairs'].append({
                        'id': i, 'question': question_text,
                        'answer': "[Respuesta no encontrada o vacía]",
                        'score': round(answer_score, 4)
                    })
            except Exception as e_inner:
                print(f"  Error extrayendo respuesta para Q{i+1} ('{question_text[:50]}...'): {e_inner}")
                results_f3['qa_pairs'].append({'id': i, 'question': question_text, 'answer': f"Error en extracción: {e_inner}", 'score': 0.0})
    except Exception as e:
        print(f"Error inicializando o usando el pipeline QA: {e}")
        existing_ids = {p['id'] for p in results_f3.get('qa_pairs', [])}
        for i, q_text in enumerate(questions): 
            if i not in existing_ids:
                results_f3['qa_pairs'].append({'id': i, 'question': q_text, 'answer': f"Error general en QA: {e}", 'score': 0.0})

    print("\n--- Resumen Resultados Fase 3 ---")
    print("Pares Pregunta-Respuesta extraídos:")
    qa_pairs_list = results_f3.get('qa_pairs', [])
    if not qa_pairs_list:
        print("  No se generaron pares Q&A.")
    else:
        for pair in qa_pairs_list:
            print(f"  Q{pair['id']+1}: {pair['question']}")
            print(f"  A{pair['id']+1}: {pair['answer']} (Score QA: {pair.get('score', 'N/A')})")
            print("-" * 10)
    print("--- Fin Fase 3 ---")
    return phase1_and_2_results

# --- Fase 4 (Evaluación de Relevancia): SIN CAMBIOS ---
def process_phase4_optional(phase1_2_and_3_results):
    print("\n--- Iniciando Fase 4 (Opcional): Cálculo de Relevancia Q&A ---")
    if not phase1_2_and_3_results or \
       'phase3_results' not in phase1_2_and_3_results or \
       'qa_pairs' not in phase1_2_and_3_results['phase3_results']:
        print("Error: Resultados de Fase 3 no disponibles o incompletos para calcular relevancia.")
        return phase1_2_and_3_results

    qa_pairs = phase1_2_and_3_results['phase3_results']['qa_pairs']
    phase1_2_and_3_results['phase4_results'] = {'qa_pairs_relevance': []}
    results_f4 = phase1_2_and_3_results['phase4_results']

    if not qa_pairs:
        print("No hay pares Q&A para calcular relevancia.")
        print("--- Fin Fase 4 ---")
        return phase1_2_and_3_results

    valid_qa_pairs = [
        p for p in qa_pairs
        if isinstance(p.get('score'), (float, int)) and p['score'] > 0.0 and \
           p.get('answer') and not p['answer'].startswith("Error") and \
           not p['answer'].startswith("[Respuesta no encontrada")
    ]

    if not valid_qa_pairs:
        print("No hay pares Q&A válidos para calcular relevancia.")
        for pair_orig in qa_pairs:
            results_f4['qa_pairs_relevance'].append({**pair_orig, 'relevance_score_%': 'N/A (Inválido o Error previo)'})
        print("--- Fin Fase 4 ---")
        return phase1_2_and_3_results

    questions = [p['question'] for p in valid_qa_pairs]
    answers = [p['answer'] for p in valid_qa_pairs]

    try:
        print("Cargando modelo Sentence Transformer para cálculo de relevancia...")
        st_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device="cpu")
        print(f"Modelo Sentence Transformer cargado (paraphrase-multilingual-mpnet-base-v2).")
        print(f"Generando embeddings para {len(valid_qa_pairs)} pares Q&A válidos...")
        q_embed = st_model.encode(questions, convert_to_tensor=True, show_progress_bar=False)
        a_embed = st_model.encode(answers, convert_to_tensor=True, show_progress_bar=False)
        print("Embeddings generados.")
        print("Calculando similitud coseno...")
        cos_scores = util.pytorch_cos_sim(q_embed, a_embed)
        
        valid_pair_rel = []
        for i, pair_valid in enumerate(valid_qa_pairs):
            sim_score = cos_scores[i][i].item()
            rel_pct = max(0.0, min(100.0, ((sim_score + 1) / 2) * 100))
            valid_pair_rel.append({**pair_valid, 'relevance_score_%': round(rel_pct, 2)})
        
        final_rel_list, valid_ids_dict = [], {p['id']: p for p in valid_pair_rel}
        for orig_pair in qa_pairs:
            pair_id = orig_pair['id']
            if pair_id in valid_ids_dict:
                final_rel_list.append(valid_ids_dict[pair_id])
            else: 
                final_rel_list.append({**orig_pair, 'relevance_score_%': 'N/A (Inválido o Error previo)'})
        
        final_rel_list.sort(key=lambda x: x['id']) 
        results_f4['qa_pairs_relevance'] = final_rel_list
        print("Cálculo de relevancia completado.")
    except Exception as e:
        print(f"Error calculando la relevancia Q&A: {e}")
        results_f4['qa_pairs_relevance'] = [{'id': p['id'], 'question': p['question'], 'answer': p['answer'], 'score': p.get('score'), 'relevance_score_%': f"Error en cálculo: {e}"} for p in qa_pairs]

    print("\n--- Resumen Resultados Fase 4 (Opcional) ---")
    print("Relevancia Pregunta-Respuesta (%):")
    qa_pairs_relevance_list = results_f4.get('qa_pairs_relevance', [])
    if not qa_pairs_relevance_list:
        print("  No se calcularon puntuaciones de relevancia.")
    else:
        for pair_rel in qa_pairs_relevance_list:
            print(f"  Q{pair_rel['id']+1}: {pair_rel['question']}")
            print(f"  A{pair_rel['id']+1}: {pair_rel['answer']}")
            print(f"  Score QA: {pair_rel.get('score', 'N/A')}")
            print(f"  Relevancia Semántica: {pair_rel.get('relevance_score_%', 'N/A')}")
            print("-" * 10)
    print("--- Fin Fase 4 ---")
    return phase1_2_and_3_results

# --- MEJORA: Función para guardar los resultados en un archivo .txt (SE MANTIENE) ---
def save_results_to_txt(final_results, input_filename):
    """
    Pregunta al usuario por una carpeta y guarda los pares de Q&A en un archivo .txt.
    """
    print("\n--- Iniciando Fase 5 (Opcional): Guardar Resultados en Archivo .txt ---")
    
    # Extraer los pares de Q&A finales (pueden venir de la fase 4 o 3)
    if 'phase4_results' in final_results and final_results['phase4_results'].get('qa_pairs_relevance'):
        qa_pairs = final_results['phase4_results']['qa_pairs_relevance']
    elif 'phase3_results' in final_results and final_results['phase3_results'].get('qa_pairs'):
        qa_pairs = final_results['phase3_results']['qa_pairs']
    else:
        print("No se encontraron pares de Pregunta/Respuesta para guardar. Omitiendo guardado.")
        return

    # Preparar la interfaz gráfica de Tkinter para el diálogo de selección de carpeta
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    
    print("Por favor, selecciona una carpeta para guardar el archivo de resultados...")
    # Abrir el diálogo para que el usuario elija una carpeta
    output_directory = filedialog.askdirectory(title="Selecciona la carpeta para guardar el archivo de resultados")

    if not output_directory:
        print("Operación cancelada por el usuario. No se guardará ningún archivo.")
        print("--- Fin Fase 5 ---")
        return

    try:
        # Construir el nombre del archivo de salida
        base_filename = os.path.basename(input_filename)
        output_filename = f"QA_{base_filename}"
        output_filepath = os.path.join(output_directory, output_filename)

        print(f"Guardando resultados en: {output_filepath}")

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Resultados de Preguntas y Respuestas para el archivo: {base_filename}\n")
            f.write("=" * 80 + "\n\n")

            for i, pair in enumerate(qa_pairs):
                f.write(f"Pregunta {i+1}:\n")
                f.write(f"{pair.get('question', '[Pregunta no disponible]')}\n\n")
                f.write(f"Respuesta {i+1}:\n")
                f.write(f"{pair.get('answer', '[Respuesta no disponible]')}\n\n")
                # Opcionalmente, añadir las puntuaciones
                score_qa = pair.get('score', 'N/A')
                score_relevance = pair.get('relevance_score_%', 'N/A')
                f.write(f"(Puntuación de Confianza de la Respuesta: {score_qa} | Relevancia Semántica: {score_relevance}%)\n")
                f.write("-" * 80 + "\n\n")

        print("¡Archivo guardado exitosamente!")

    except Exception as e:
        print(f"Error: No se pudo guardar el archivo. Razón: {e}")
    
    print("--- Fin Fase 5 ---")


# --- Bloque Principal de Ejecución (SIN CAMBIOS) ---
if __name__ == "__main__":
    print("--- Iniciando Pipeline NLP Completo ---")
    phase1_results = process_phase1(INPUT_TEXT_FILE_PATH)
    
    phase1_and_2_results = None
    if phase1_results and phase1_results.get("language") in ['en', 'es']:
        phase1_and_2_results = process_phase2(phase1_results)
    elif phase1_results: 
        print("\nProceso detenido después de Fase 1: Idioma no soportado para Fases 2+.")
        phase1_and_2_results = phase1_results 
    else: 
        print("\nEl proceso no pudo continuar debido a errores críticos en la Fase 1.")
    
    phase1_2_and_3_results = None
    if phase1_and_2_results and \
       'phase2_results' in phase1_and_2_results and \
       isinstance(phase1_and_2_results['phase2_results'].get('generated_questions'), list) and \
       len(phase1_and_2_results['phase2_results']['generated_questions']) > 0 :
        phase1_2_and_3_results = process_phase3(phase1_and_2_results)
    elif phase1_and_2_results: 
        print("\nOmitiendo Fase 3 (No hay preguntas válidas de Fase 2 o error previo).")
        phase1_2_and_3_results = phase1_and_2_results
        
    final_results = phase1_2_and_3_results 
    if phase1_2_and_3_results and \
       'phase3_results' in phase1_2_and_3_results and \
       isinstance(phase1_2_and_3_results['phase3_results'].get('qa_pairs'), list) and \
       phase1_2_and_3_results['phase3_results']['qa_pairs']:
        final_results = process_phase4_optional(phase1_2_and_3_results)
    elif phase1_2_and_3_results: 
        print("\nOmitiendo Fase 4 (No hay pares Q&A válidos de Fase 3 o error previo).")
    
    print("\n--- Fin del Pipeline NLP Completo ---")
    print("\n--- Resumen Final (Datos Principales) ---")
    if final_results:
        print(f"Archivo Procesado: {INPUT_TEXT_FILE_PATH}")
        print(f"Idioma Detectado: {final_results.get('language', 'N/A')}")
        if 'phase2_results' in final_results and isinstance(final_results['phase2_results'].get('generated_questions'), list):
            print(f"Preguntas Generadas: {len(final_results['phase2_results']['generated_questions'])}")
        if 'phase3_results' in final_results and isinstance(final_results['phase3_results'].get('qa_pairs'), list):
            print(f"Pares Q&A Extraídos: {len(final_results['phase3_results']['qa_pairs'])}")
        if 'phase4_results' in final_results and isinstance(final_results['phase4_results'].get('qa_pairs_relevance'), list):
            print(f"Pares Q&A con Relevancia: {len(final_results['phase4_results']['qa_pairs_relevance'])}")
        
        # Se mantiene la llamada a la función de guardado
        save_results_to_txt(final_results, INPUT_TEXT_FILE_PATH)

    else:
        print("\nNo se generaron resultados finales completos debido a errores previos.")