<p align="center">
  <img src="assets/Banner.png" width="100%">
</p>

<h1 align="center">
📖 Analíticas de Lectura Inteligente
</h1>

<p align="center">
Potenciando el Aprendizaje con Inteligencia Artificial
</p>

## 🎯 Descripción

Este proyecto fue desarrollado como trabajo de tesis para la obtención del grado de Ingeniería en Tecnologías de la Información.

Su propósito es aplicar técnicas de Inteligencia Artificial y Procesamiento de Lenguaje Natural (NLP) para fortalecer la comprensión lectora mediante el análisis automatizado de documentos, la generación de preguntas y la evaluación semántica de las respuestas del usuario.

La herramienta está dirigida principalmente a estudiantes como apoyo autodidacta, aunque también puede ser utilizada por docentes para identificar oportunidades de mejora en el aprendizaje de sus alumnos.

## 💡 Problema que resuelve

Actualmente, muchos estudiantes presentan dificultades para comprender, analizar e interpretar la información que leen, lo que afecta su capacidad para construir conocimiento y generar ideas propias.

Este proyecto busca apoyar dicho proceso mediante una herramienta inteligente capaz de:


- Analizar documentos PDF.
- Detectar automáticamente el idioma.
- Traducir el contenido cuando es necesario.
- Generar resúmenes.
- Crear preguntas automáticamente.
- Evaluar respuestas utilizando modelos de IA.
- Medir la coherencia semántica entre pregunta y respuesta.
- Generar reportes con métricas de desempeño.

## ✨ Objetivos

### Objetivo General

Desarrollar una herramienta basada en Inteligencia Artificial y Procesamiento de Lenguaje Natural capaz de fortalecer la comprensión lectora mediante el análisis automático de documentos, la generación de preguntas y la evaluación semántica de respuestas.

### Objetivos específicos

- Detectar automáticamente el idioma del documento.
- Analizar el contenido mediante técnicas de NLP.
- Extraer los temas principales del texto.
- Generar preguntas de manera automática.
- Evaluar la coherencia semántica de las respuestas.
- Generar métricas que apoyen el aprendizaje del estudiante.

## 🚀 Funcionamiento general
1. El usuario carga un documento.
2. El sistema analiza el contenido.
3. Se identifican los temas principales.
4. Se generan preguntas automáticamente.
5. El usuario responde.
6. La IA analiza las respuestas.
7. Se genera un reporte con métricas.
   
## 🧠 Arquitectura de IA

| Modelo | Función |
|---------|----------|
| spaCy | Procesamiento del lenguaje |
| NLTK | Tokenización |
| YAKE | Extracción de palabras clave |
| LDA | Detección de temas |
| T5 | Generación automática de preguntas |
| RoBERTa QA | Extracción de respuestas |
| Sentence Transformers | Evaluación semántica |
| fast-langdetect | Detección del idioma |

## 📊 Arquitectura del Sistema

El  siguiente diagrama muestra el flujo completo del sistema desarrollado, desde la carga del documento hasta la generación del reporte final. Cada etapa representa un módulo del pipeline de Procesamiento de Lenguaje Natural (NLP) y los modelos de Inteligencia Artificial utilizados durante el análisis.

<p align="center">
  <img src= "assets/Diagrama.png" width="100%">
</p>

El sistema inicia con la carga del documento, realiza el preprocesamiento y la detección automática del idioma. Posteriormente ejecuta un pipeline de NLP que incluye tokenización, procesamiento lingüístico, extracción de palabras clave, modelado de temas y generación de resúmenes. Finalmente genera preguntas, analiza las respuestas del usuario mediante RoBERTa QA, calcula la similitud semántica utilizando Sentence Transformers y produce un reporte con métricas y analíticas del aprendizaje.
---

## 📂 Estructura del proyecto

```text
analiticas_lectura_inteligente_ia
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── assets/
│   ├── Banner.png
│   ├── Diagrama.png
│   ├── interfazGrafica.jpeg
│   └── Reporte.jpeg
│
├── src/
│   ├── main.py
│   ├── preprocessing.py
│   ├── language_detector.py
│   ├── topic_model.py
│   ├── question_generator.py
│   ├── answer_extractor.py
│   ├── semantic_similarity.py
│   └── report_generator.py
│
└── examples/
```

## 🛠 Tecnologías

- Python
- VS Code
- Anaconda
- Spyder
- Google Colab
- Hugging Face
- PyTorch
## ⚙️ Instalación

Clonar el repositorio

```bash
git clone https://github.com/citlallimt/analiticas_lectura_inteligente_ia.git
```

Entrar al proyecto

```bash
cd analiticas_lectura_inteligente_ia
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Ejecutar

```bash
python src/main.py
```
## 📊 Resultados generados

El sistema produce automáticamente:

- Idioma detectado
- Métricas del documento
- Complejidad léxica
- Análisis de sentimiento
- Palabras clave
- Tópicos principales
- Preguntas generadas
- Respuestas automáticas
- Similitud semántica
- Reporte TXT

  ## 🖥️ Interfaz del sistema

La aplicación cuenta con una interfaz gráfica que permite cargar documentos, ejecutar el análisis completo y visualizar cada una de las fases del procesamiento.

<p align="center">
  <img src="assets/interfazGrafica.jpeg" width="90%">
</p>

## 📄 Reporte generado

Al finalizar el análisis, el sistema genera automáticamente un archivo de texto (.txt) que reúne los resultados obtenidos durante todo el proceso.

El reporte incluye las preguntas elaboradas automáticamente, las respuestas extraídas del documento y los indicadores de evaluación, como la puntuación de confianza y la relevancia semántica. Este recurso incrementa la portabilidad y la aplicabilidad práctica del prototipo, ya que facilita el almacenamiento, la consulta y la integración de la información en otros medios digitales o impresos.

<p align="center">
  <img src="assets/Reporte.jpeg" width="90%">
</p>

  
## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.

## 👤 Autor

**Citlalli M. T.**

Proyecto desarrollado como trabajo de tesis para la obtención del grado de Ingeniería en Tecnologías de la Información.

## 📈 Estado del proyecto

✅ Proyecto de tesis finalizado.

Actualmente se encuentra en proceso de documentación y organización para su publicación como portafolio profesional en GitHub.

En futuras versiones se contempla incorporar nuevas funcionalidades enfocadas en analítica educativa, evaluación del aprendizaje y mejora de la interacción mediante Inteligencia Artificial.

📌 Nota: Este proyecto fue desarrollado con fines académicos para la obtención del título de Ingeniería en Tecnologías de la Información en la Universidad Politecnica Metropolitana de Hidalgo . El código se comparte exclusivamente de forma pública con fines de demostración de competencias profesionales y portafolio laboral.
