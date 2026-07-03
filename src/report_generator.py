"""
Módulo encargado de generar el reporte final
con los resultados del análisis.

Funciones:
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
        Ruta de la carpeta seleccionada.
    """

    root = Tk()
    root.withdraw()

    directory = filedialog.askdirectory(
        title="Selecciona la carpeta para guardar el reporte"
    )

    return directory
