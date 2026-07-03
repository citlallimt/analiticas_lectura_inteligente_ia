"""
Módulo encargado de generar el reporte final
con los resultados del análisis.

Funciones:
- Selección de carpeta.
- Exportación de resultados.
- Generación del archivo de salida.
"""

import os
from tkinter import Tk, filedialog


def select_output_directory():
    """
    Permite seleccionar la carpeta donde
    se guardará el reporte final.

    Retorna
    -------
    str
        Ruta seleccionada.
    """

    root = Tk()
    root.withdraw()

    directory = filedialog.askdirectory(
        title="Selecciona la carpeta donde guardar el reporte"
    )

    return directory


def save_report(
    input_file: str,
    metrics: dict,
    complexity: float,
    sentiment: dict,
    keywords: list,
    topics: dict,
    qa_pairs: list
):
    """
    Guarda el reporte completo en un archivo TXT.

    Parámetros
    ----------
    input_file : str
        Documento analizado.

    metrics : dict
        Métricas del documento.

    complexity : float
        Complejidad léxica.

    sentiment : dict
        Resultado del análisis de sentimiento.

    keywords : list
        Palabras clave.

    topics : dict
        Tópicos encontrados.

    qa_pairs : list
        Preguntas, respuestas y relevancia.
    """

    directory = select_output_directory()

    if not directory:

        print("No se seleccionó carpeta.")

        return

    filename = os.path.basename(input_file)

    output_file = os.path.join(
        directory,
        f"Reporte_{filename}"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("=" * 80 + "\n")
        file.write("ANALÍTICAS DE LECTURA INTELIGENTE\n")
        file.write("=" * 80 + "\n\n")

        file.write("MÉTRICAS\n")
        file.write(str(metrics))
        file.write("\n\n")

        file.write(
            f"Complejidad léxica: {complexity}\n\n"
        )

        file.write(
            f"Sentimiento: {sentiment}\n\n"
        )

        file.write("PALABRAS CLAVE\n")

        for keyword in keywords:
            file.write(f"- {keyword}\n")

        file.write("\n")

        file.write("TÓPICOS\n")

        for topic, words in topics.items():
            file.write(f"{topic}: {words}\n")

        file.write("\n")

        file.write("PREGUNTAS Y RESPUESTAS\n\n")

        for pair in qa_pairs:

            file.write(
                f"Pregunta {pair['id'] + 1}\n"
            )

            file.write(pair["question"] + "\n\n")

            file.write(
                "Respuesta:\n"
            )

            file.write(pair["answer"] + "\n\n")

            file.write(
                f"Score QA: {pair['score']}\n"
            )

            file.write(
                f"Relevancia: {pair['relevance_score']}%\n"
            )

            file.write("-" * 80 + "\n")

    print(f"\nReporte guardado en:\n{output_file}")
