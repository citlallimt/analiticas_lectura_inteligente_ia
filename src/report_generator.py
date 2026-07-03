"""
Módulo encargado de generar el reporte final
con los resultados del análisis.

Funciones:
- Selección de la carpeta de salida.
- Generación del archivo de resultados.
- Exportación del reporte.
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
        Ruta de la carpeta seleccionada.
    """

    root = Tk()
    root.withdraw()

    directory = filedialog.askdirectory(
        title="Selecciona la carpeta para guardar el reporte"
    )

    return directory


def save_report(qa_pairs: list, input_filename: str):
    """
    Guarda el reporte final en un archivo de texto.

    Parámetros
    ----------
    qa_pairs : list
        Lista de preguntas y respuestas.

    input_filename : str
        Nombre del documento procesado.
    """

    output_directory = select_output_directory()

    if not output_directory:
        print("No se seleccionó ninguna carpeta.")
        return

    output_file = os.path.join(
        output_directory,
        f"QA_{os.path.basename(input_filename)}"
    )

    with open(output_file, "w", encoding="utf-8") as file:

        file.write(
            f"Resultados del documento: {input_filename}\n"
        )

        file.write("=" * 80)
        file.write("\n\n")

        for index, pair in enumerate(qa_pairs):

            file.write(
                f"Pregunta {index+1}\n"
            )

            file.write(
                pair["question"] + "\n\n"
            )

            file.write(
                f"Respuesta {index+1}\n"
            )

            file.write(
                pair["answer"] + "\n\n"
            )

            if "score" in pair:

                file.write(
                    f"Confianza QA: {pair['score']}\n"
                )

            if "semantic_similarity" in pair:

                file.write(
                    f"Similitud semántica: "
                    f"{pair['semantic_similarity']}%\n"
                )

            file.write("-" * 80)
            file.write("\n\n")

    print(f"Reporte guardado en:\n{output_file}")
