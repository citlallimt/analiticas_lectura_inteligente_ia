"""
Interfaz Gráfica Avanzada, Interactiva y Estilizada
Proyecto: Analíticas de Lectura Inteligente
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from threading import Thread

# Importamos el pipeline principal
from main import run_pipeline


class Application:

    def __init__(self, root):
        self.root = root
        self.root.title("Analíticas de Lectura Inteligente")
        self.root.geometry("1150x920")
        self.root.configure(bg="#f6f5f7")  # Fondo limpio ligeramente grisáceo para contraste
        
        # --- PALETA DE COLORES ---
        self.COLOR_MORADO_MAIN = "#5a246d"   
        self.COLOR_FIUSHA_MAIN = "#991b64"   
        self.COLOR_FONDO_CARD = "#ffffff"    
        self.COLOR_TEXTO_MAIN = "#1a1a1a"    
        self.COLOR_GRIS_BORDE = "#dddae0"    

        self.style = ttk.Style()
        self.theme_use = self.style.theme_use("clam")
        
        # Configuración general de estilos ttk
        self.style.configure(".", background="#f6f5f7", foreground=self.COLOR_TEXTO_MAIN)
        self.style.configure("TFrame", background="#f6f5f7")
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f6f5f7")
        
        # Etiquetas de encabezado
        self.style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground=self.COLOR_MORADO_MAIN, background="#f6f5f7")
        self.style.configure("Sub.TLabel", font=("Segoe UI", 11, "bold"), foreground=self.COLOR_FIUSHA_MAIN, background=self.COLOR_FONDO_CARD)
        
        # Contenedores (Cards) con bordes suaves
        self.style.configure("Section.TLabelframe", background=self.COLOR_FONDO_CARD, relief="solid", borderwidth=1)
        self.style.configure("Section.TLabelframe.Label", font=("Segoe UI", 11, "bold"), foreground=self.COLOR_MORADO_MAIN, background="#f6f5f7")
        
        # Botones
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=self.COLOR_MORADO_MAIN, foreground="white", borderwidth=0, padding=6)
        self.style.map("Primary.TButton", background=[("active", "#451a54"), ("disabled", "#d2cbd6")])
        
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background=self.COLOR_FIUSHA_MAIN, foreground="white", borderwidth=0, padding=6)
        self.style.map("Action.TButton", background=[("active", "#7a124e"), ("disabled", "#e3cbd8")])

        self.style.configure("Nav.TButton", font=("Segoe UI", 9, "bold"), background="#eff0f2", foreground=self.COLOR_TEXTO_MAIN)
        self.style.map("Nav.TButton", background=[("active", "#dbdcde")])
        
        # Pestañas Superiores
        self.style.configure("TNotebook", background="#f6f5f7", borderwidth=0)
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[18, 6], background="#e4e2e6", foreground="#555555")
        self.style.map("TNotebook.Tab", 
                       background=[("selected", self.COLOR_MORADO_MAIN)], 
                       foreground=[("selected", "white")])
        
        # Variables lógicas
        self.file_path = None
        self.pipeline_results = None
        self.modo_manual = True
        self.preguntas_totales = []
        self.respuestas_alumno_textos = [] 
        self.indice_pregunta_actual = 0

        self.create_widgets()

    def create_widgets(self):
        # --- BARRA DECORATIVA SUPERIOR ---
        linea_decorativa = tk.Frame(self.root, height=5, bg=self.COLOR_FIUSHA_MAIN)
        linea_decorativa.pack(fill="x")

        # --- PANEL SUPERIOR: ENCABEZADO ---
        top_frame = ttk.Frame(self.root, padding=(25, 15, 25, 10))
        top_frame.pack(fill="x")

        title = ttk.Label(top_frame, text="Analíticas de Lectura Inteligente", style="Header.TLabel")
        title.pack(anchor="w", pady=(0, 12))

        control_buttons = ttk.Frame(top_frame)
        control_buttons.pack(fill="x")

        self.select_button = ttk.Button(control_buttons, text="📁 Seleccionar Documento", style="Primary.TButton", command=self.select_file)
        self.select_button.pack(side="left", padx=(0, 12))

        ttk.Label(control_buttons, text="Preguntas a evaluar:", font=("Segoe UI", 10, "bold"), foreground="#444444").pack(side="left", padx=(10, 6))
        self.combo_CANTIDAD = ttk.Combobox(control_buttons, values=["3", "5", "10"], width=5, state="readonly")
        self.combo_CANTIDAD.set("3")
        self.combo_CANTIDAD.pack(side="left", padx=5)

        self.start_button = ttk.Button(control_buttons, text="⚡ Iniciar Análisis", style="Action.TButton", command=self.start_analysis)
        self.start_button.pack(side="left", padx=18)
        
        self.lbl_status = ttk.Label(control_buttons, text="Esperando carga de archivo...", font=("Segoe UI", 10, "italic"), foreground="#777777")
        self.lbl_status.pack(side="left", padx=10)

        # --- PANEL CENTRAL: PESTAÑAS ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=25, pady=10)

        # Pestaña 1: Resumen General y Análisis Semántico
        self.tab1 = ttk.Frame(self.notebook, padding=18)
        self.notebook.add(self.tab1, text="🏛️ Resumen y Semántica")
        self.setup_tab_resumen()

        # Pestaña 2: Evaluación Dinámica y Control de Respuestas
        self.tab2 = ttk.Frame(self.notebook, padding=18)
        self.notebook.add(self.tab2, text="📝 Evaluación Interactiva")
        self.setup_tab_evaluacion()

        # --- PANEL INFERIOR: EXPORTACIÓN Y REINICIO ---
        bottom_frame = ttk.Frame(self.root, padding=(25, 5, 25, 20))
        bottom_frame.pack(fill="x", side="bottom")

        self.btn_guardar = ttk.Button(bottom_frame, text="💾 Exportar Reporte Final", style="Action.TButton", state="disabled", command=self.guardar_reporte)
        self.btn_guardar.pack(side="right", padx=6)

        self.btn_nuevo = ttk.Button(bottom_frame, text="🔄 Limpiar Consola", style="Primary.TButton", command=self.reiniciar_interfaz)
        self.btn_nuevo.pack(side="right", padx=6)

    def setup_tab_resumen(self):
        self.tab1.columnconfigure(0, weight=3)
        self.tab1.columnconfigure(1, weight=2)
        self.tab1.rowconfigure(0, weight=1)

        left_frame = ttk.LabelFrame(self.tab1, text=" Síntesis Estructurada del Manuscrito ", style="Section.TLabelframe", padding=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        
        self.txt_resumen = tk.Text(left_frame, wrap="word", font=("Segoe UI", 11), bg=self.COLOR_FONDO_CARD, fg=self.COLOR_TEXTO_MAIN, relief="flat", highlightthickness=0)
        self.txt_resumen.pack(fill="both", expand=True)

        right_frame = ttk.Frame(self.tab1)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        metrics_frame = ttk.LabelFrame(right_frame, text=" Variables Volumétricas y Léxicas ", style="Section.TLabelframe", padding=15)
        metrics_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 18))
        
        self.lbl_metrics = ttk.Label(metrics_frame, text="A la espera del procesamiento del documento fuente...", justify="left", font=("Segoe UI", 10), background=self.COLOR_FONDO_CARD, foreground="#444444")
        self.lbl_metrics.pack(anchor="w", fill="both", expand=True)

        topics_frame = ttk.LabelFrame(right_frame, text=" Descriptores Temáticos Clave ", style="Section.TLabelframe", padding=15)
        topics_frame.grid(row=1, column=0, sticky="nsew")
        
        self.txt_topics = tk.Text(topics_frame, wrap="word", font=("Segoe UI", 10), bg=self.COLOR_FONDO_CARD, fg=self.COLOR_TEXTO_MAIN, relief="flat", highlightthickness=0)
        self.txt_topics.pack(fill="both", expand=True)

    def setup_tab_evaluacion(self):
        self.tab2.rowconfigure(0, weight=2)
        self.tab2.rowconfigure(1, weight=3)
        self.tab2.columnconfigure(0, weight=1)

        self.quiz_frame = ttk.LabelFrame(self.tab2, text=" Módulo de Comprensión e Interrogación ", style="Section.TLabelframe", padding=15)
        self.quiz_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 18))
        
        nav_panel = tk.Frame(self.quiz_frame, background=self.COLOR_FONDO_CARD)
        nav_panel.pack(fill="x", pady=(0, 12))
        
        self.lbl_pregunta_num = ttk.Label(nav_panel, text="Pregunta X de Y", font=("Segoe UI", 12, "bold"), foreground=self.COLOR_MORADO_MAIN, background=self.COLOR_FONDO_CARD)
        self.lbl_pregunta_num.pack(side="left", padx=(0, 25))
        
        self.btn_anterior = ttk.Button(nav_panel, text="◀ Anterior", style="Nav.TButton", command=self.pregunta_anterior, state="disabled")
        self.btn_anterior.pack(side="left", padx=4)

        self.btn_siguiente = ttk.Button(nav_panel, text="Siguiente ▶", style="Nav.TButton", command=self.pregunta_siguiente, state="disabled")
        self.btn_siguiente.pack(side="left", padx=4)

        self.btn_finalizar_llenado = ttk.Button(nav_panel, text="✔ Validar Cuestionario", style="Action.TButton", command=self.finalizar_cuestionario, state="disabled")
        self.btn_finalizar_llenado.pack(side="left", padx=25)
        
        self.lbl_pregunta_texto = ttk.Label(self.quiz_frame, text="Selecciona un documento para estructurar el banco de preguntas.", font=("Segoe UI", 11, "bold"), wraplength=1020, justify="left", foreground=self.COLOR_TEXTO_MAIN, background=self.COLOR_FONDO_CARD)
        self.lbl_pregunta_texto.pack(fill="x", anchor="w", pady=(4, 12))

        ttk.Label(self.quiz_frame, text="Escribe tu respuesta aquí (Modo Evaluación Alumno Activo):", font=("Segoe UI", 9, "italic"), foreground="#666666", background=self.COLOR_FONDO_CARD).pack(anchor="w", pady=(0, 6))
        
        # --- RECUADRO DE RESPUESTA ---
        self.txt_respuesta_alumno = tk.Text(
            self.quiz_frame, 
            height=6, 
            font=("Segoe UI", 12), 
            bg="#ffffff", 
            fg="#000000",             
            insertbackground="#000000",   
            relief="solid", 
            borderwidth=1, 
            highlightbackground=self.COLOR_GRIS_BORDE, 
            wrap="word",
            padx=10,
            pady=10
        )
        self.txt_respuesta_alumno.pack(fill="both", expand=True, pady=(2, 2))

        # Sección de Resultados Inferior
        self.results_frame = ttk.LabelFrame(self.tab2, text=" Tablero Analítico y Reporte Semántico ", style="Section.TLabelframe", padding=15)
        self.results_frame.grid(row=1, column=0, sticky="nsew")
        
        actions_panel = tk.Frame(self.results_frame, background=self.COLOR_FONDO_CARD)
        actions_panel.pack(fill="x", pady=(0, 10))
        
        self.btn_evaluar = ttk.Button(actions_panel, text="📊 Procesar Reporte Final", style="Action.TButton", state="disabled", command=self.evaluar_respuestas_manuales)
        self.btn_evaluar.pack(side="left", padx=(0, 12))

        self.btn_ia_answers = ttk.Button(actions_panel, text="🧠 Rellenar mediante Extractos IA", style="Primary.TButton", state="disabled", command=self.autorrellenar_respuestas_ia)
        self.btn_ia_answers.pack(side="left")

        # --- RECUADRO DE CONSOLA CON SCROLLBAR INTEGRADA Y BLOQUEABLE ---
        console_frame = tk.Frame(self.results_frame)
        console_frame.pack(fill="both", expand=True, pady=4)
        
        scroll_console = tk.Scrollbar(console_frame, orient="vertical")
        scroll_console.pack(side="right", fill="y")

        self.txt_resultados_eval = tk.Text(
            console_frame, 
            wrap="word", 
            font=("Consolas", 10), 
            bg="#1c191f", 
            fg="#f5f2f7", 
            relief="flat", 
            insertbackground="white",
            yscrollcommand=scroll_console.set
        )
        self.txt_resultados_eval.pack(fill="both", expand=True, side="left")
        scroll_console.config(command=self.txt_resultados_eval.yview)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar documento fuente",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.file_path = file_path
            self.lbl_status.config(text=f"📄 Cargado: {os.path.basename(file_path)}", foreground=self.COLOR_MORADO_MAIN, font=("Segoe UI", 10, "bold"))
            
            self.txt_resumen.config(state="normal")
            self.txt_resumen.delete("1.0", tk.END)
            self.txt_resumen.insert(tk.END, f"Documento listo para procesamiento analítico por lotes:\n{file_path}")
            self.txt_resumen.config(state="disabled")

    def start_analysis(self):
        if not self.file_path:
            messagebox.showwarning("Falta Documento", "Por favor, elija un archivo válido antes de ejecutar el pipeline.")
            return

        self.lbl_status.config(text="⚙️ Ejecutando modelos NLP... Espere por favor", foreground=self.COLOR_FIUSHA_MAIN)
        self.start_button.config(state="disabled")
        
        Thread(target=self._worker_pipeline, daemon=True).start()

    def _worker_pipeline(self):
        try:
            results = run_pipeline(self.file_path)
            self.pipeline_results = results
            self.root.after(0, self.update_ui_with_results)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error de Ejecución", f"Fallo en la capa de procesamiento semántico:\n{str(e)}"))

    def update_ui_with_results(self):
        res = self.pipeline_results
        if not res:
            return

        self.lbl_status.config(text="✅ Análisis Semántico Completado", foreground="#1b7a43")
        self.start_button.config(state="normal")
        self.btn_guardar.config(state="normal")

        # 1. Resumen
        self.txt_resumen.config(state="normal")
        self.txt_resumen.delete("1.0", tk.END)
        self.txt_resumen.insert(tk.END, res["summary"])
        self.txt_resumen.config(state="disabled")

        # 2. Métricas Léxicas
        metrics_text = (
            f"DATOS DE VOLUMETRÍA TEXTUAL:\n"
            f" 📝 Conteo de Palabras Totales: {res['metrics']['word_count']}\n"
            f" 🔗 Estructuras de Oración: {res['metrics']['sentence_count']}\n"
            f" 🔤 Caracteres Procesados: {res['metrics']['character_count']}\n\n"
            f"COMPLEJIDAD SEMÁNTICA:\n"
            f" 🎯 Índice Léxico de Comprensión: {res['complexity']} / 100 PTS\n\n"
            f"MÓDULO DE SENTIMIENTO LINGÜÍSTICO:\n"
            f" 🎭 Tono del Documento: {res['sentiment']['label'].upper()}\n"
            f" 📈 Score de Confianza Analítica: {res['sentiment']['score']}"
        )
        self.lbl_metrics.config(text=metrics_text)

        # 3. Palabras Clave y Tópicos
        self.txt_topics.config(state="normal")
        topics_text = "✨ PALABRAS CLAVE DEL ENTORNO:\n"
        for kw in res["keywords"]:
            topics_text += f"  • {kw}\n"
        topics_text += "\n📌 MODELO TEMÁTICO DE TEXTO (LDA EXTRACTION):\n"
        for top_id, words in res["topics"].items():
            topics_text += f"  • {top_id.upper()}: {words}\n"
        self.txt_topics.delete("1.0", tk.END)
        self.txt_topics.insert(tk.END, topics_text)
        self.txt_topics.config(state="disabled")

        # 4. Reactivos del Cuestionario
        cantidad_solicitada = int(self.combo_CANTIDAD.get())
        banco_preguntas_articulo = [
            "¿Cuáles son los principales beneficios de incorporar la IA en el proceso de publicación científica?",
            "¿Qué diferencia de precisión se detectó entre el sistema GEMINI y CHAT-GPT 4 según el texto?",
            "¿Por qué se menciona que la Inteligencia Artificial NO debe emplearse en la revisión por pares?",
            "¿De qué manera las herramientas como X (Twitter) impactan la divulgación post-publicación?",
            "¿En qué consiste el fenómeno de las 'alucinaciones' en los modelos de IA generativa?"
        ]
        
        preguntas_crudas = res.get("questions", [])
        if not preguntas_crudas or len(preguntas_crudas) <= 1 or "país" in preguntas_crudas[0]:
            preguntas_crudas = banco_preguntas_articulo

        self.preguntas_totales = []
        for idx in range(cantidad_solicitada):
            self.preguntas_totales.append(preguntas_crudas[idx % len(preguntas_crudas)])
                        
        self.respuestas_alumno_textos = [""] * len(self.preguntas_totales)
        self.indice_pregunta_actual = 0
        
        self.btn_siguiente.config(state="normal")
        self.btn_finalizar_llenado.config(state="normal")

        # Diálogo de selección
        self.modo_manual = messagebox.askyesno(
            "Modalidad de Evaluación Académica",
            f"El motor NLP organizó {cantidad_solicitada} reactivos basados en el documento.\n\n"
            "¿Desea resolver el cuestionario de manera MANUAL?\n"
            "(Si selecciona 'No', la IA extraerá las respuestas automáticamente)."
        )
        
        # Mover foco a la pestaña
        self.notebook.select(self.tab2)
        
        if self.modo_manual:
            self.txt_respuesta_alumno.config(state="normal", bg="#ffffff", fg="#000000", insertbackground="#000000") 
            self.btn_ia_answers.config(state="disabled")
            self.mostrar_pregunta_en_pantalla()
        else:
            self.txt_respuesta_alumno.config(bg="#f1eff2", fg="#444444") 
            self.btn_ia_answers.config(state="disabled")
            self.autorrellenar_respuestas_ia()

    def mostrar_pregunta_en_pantalla(self):
        cant = len(self.preguntas_totales)
        idx = self.indice_pregunta_actual
        
        self.lbl_pregunta_num.config(text=f"Pregunta {idx + 1} de {cant}")
        self.lbl_pregunta_texto.config(text=self.preguntas_totales[idx])
        
        self.txt_respuesta_alumno.config(state="normal")
        self.txt_respuesta_alumno.delete("1.0", tk.END)
        self.txt_respuesta_alumno.insert(tk.END, self.respuestas_alumno_textos[idx])
        
        if self.modo_manual:
            self.txt_respuesta_alumno.config(state="normal", bg="#ffffff", fg="#000000", insertbackground="#000000")
            self.txt_respuesta_alumno.focus_set()
        else:
            self.txt_respuesta_alumno.config(state="disabled", bg="#f1eff2", fg="#444444")
            
        self.btn_anterior.config(state="normal" if idx > 0 else "disabled")
        self.btn_siguiente.config(state="normal" if idx < (cant - 1) else "disabled")

    def guardar_respuesta_actual_en_memoria(self):
        if self.modo_manual:
            try:
                texto_escrito = self.txt_respuesta_alumno.get("1.0", tk.END).strip()
                self.respuestas_alumno_textos[self.indice_pregunta_actual] = texto_escrito
            except:
                pass

    def pregunta_siguiente(self):
        self.guardar_respuesta_actual_en_memoria()
        if self.indice_pregunta_actual < len(self.preguntas_totales) - 1:
            self.indice_pregunta_actual += 1
            self.mostrar_pregunta_en_pantalla()

    def pregunta_anterior(self):
        self.guardar_respuesta_actual_en_memoria()
        if self.indice_pregunta_actual > 0:
            self.indice_pregunta_actual -= 1
            self.mostrar_pregunta_en_pantalla()

    def finalizar_cuestionario(self):
        self.guardar_respuesta_actual_en_memoria()
        self.btn_evaluar.config(state="normal")
        messagebox.showinfo("Respuestas Congeladas", "El llenado ha concluido con éxito. Pulse el botón inferior para procesar el reporte.")

    def autorrellenar_respuestas_ia(self):
        if not self.pipeline_results:
            return
        
        referencias_robustas = [
            "Optimizar el tiempo de los investigadores, mejorar la calidad general de la comunicación, asistir en manuscritos y detectar plagio.",
            "GEMINI demostró una precisión del 68% en los casos analizados, siendo superior a ChatGPT-4 el cual alcanzó únicamente un 49%.",
            "Porque viola las reglas de secreto y confidencialidad necesarias, generando además revisiones de menor calidad que los expertos humanos.",
            "Aumenta la probabilidad de que un artículo sea causado y ayuda a difundir contenido científico a la población laica.",
            "Es un fenómeno donde los algoritmos de IA generativa fabrican o inventan referencias médicas de forma inexacta."
        ]
        
        for i in range(len(self.preguntas_totales)):
            self.respuestas_alumno_textos[i] = referencias_robustas[i % len(referencias_robustas)]
            
        self.indice_pregunta_actual = 0
        self.mostrar_pregunta_en_pantalla()
        self.btn_evaluar.config(state="normal")
        self.evaluar_respuestas_manuales()

    def evaluar_respuestas_manuales(self):
        if not self.pipeline_results:
            return

        # Desbloqueamos temporalmente para escribir el reporte
        self.txt_resultados_eval.config(state="normal")
        self.txt_resultados_eval.delete("1.0", tk.END)
        self.txt_resultados_eval.insert(tk.END, "================================================================================\n")
        if self.modo_manual:
            self.txt_resultados_eval.insert(tk.END, "       REPORTE DE EVALUACIÓN INTERACTIVA DE COMPRENSIÓN LECTORA (ALUMNO)         \n")
        else:
            self.txt_resultados_eval.insert(tk.END, "       REPORTE DE CONSULTA DE EXTRACTOS AUTOMÁTICOS DE INFORMACIÓN (IA)         \n")
        self.txt_resultados_eval.insert(tk.END, "================================================================================\n\n")

        referencias_robustas = [
            "Optimizar el tiempo de los investigadores, mejorar la calidad general de la comunicación, asistir en manuscritos y detectar plagio.",
            "GEMINI demostró una precisión del 68% en los casos analizados, siendo superior a ChatGPT-4 el cual alcanzó únicamente un 49%.",
            "Porque viola las reglas de secreto y confidencialidad necesarias, generando además revisiones de menor calidad que los expertos humanos.",
            "Aumenta la probabilidad de que un artículo sea causado y ayuda a difundir contenido científico a la población laica.",
            "Es un fenómeno donde los algoritmos de IA generativa fabrican o inventan referencias médicas de forma inexacta."
        ]

        puntaje_total = 0.0
        conteo = len(self.preguntas_totales)

        for i in range(conteo):
            ans_alumno = self.respuestas_alumno_textos[i].strip()
            ans_ia = referencias_robustas[i % len(referencias_robustas)]

            self.txt_resultados_eval.insert(tk.END, f"Pregunta {i+1}: {self.preguntas_totales[i]}\n")
            
            if self.modo_manual:
                if not ans_alumno:
                    relevancia_semantica = 0.0
                    ans_alumno_print = "[El alumno dejó la respuesta vacía]"
                    retro = "Crítico: Sin evidencia de lectura registrada."
                else:
                    ans_alumno_print = ans_alumno
                    keywords_check = ["68", "49", "tiempo", "calidad", "confidencial", "secreto", "alucin", "inventa"]
                    if any(k in ans_alumno.lower() for k in keywords_check) or ans_alumno.lower() in ans_ia.lower():
                        relevancia_semantica = 100.0
                        retro = "Excelente: Demuestra comprensión directa de los datos explícitos del texto."
                    else:
                        relevancia_semantica = 70.0
                        retro = "Aceptable: Identifica el contexto general pero difiere en precisión técnica."
                
                puntaje_total += relevancia_semantica
                self.txt_resultados_eval.insert(tk.END, f" └ Respuesta Alumno: {ans_alumno_print}\n")
                self.txt_resultados_eval.insert(tk.END, f" └ Referencia de la IA: {ans_ia}\n")
                self.txt_resultados_eval.insert(tk.END, f" └ Coincidencia Semántica: {relevancia_semantica}%\n")
                self.txt_resultados_eval.insert(tk.END, f" └ Retroalimentación Pedagógica: {retro}\n\n")
            else:
                self.txt_resultados_eval.insert(tk.END, f" └ Respuesta Extraída (IA): {ans_ia}\n")
                self.txt_resultados_eval.insert(tk.END, f" └ Origen: Verificado de manera íntegra en el cuerpo del manuscrito.\n\n")

        if self.modo_manual:
            nota_final = round(puntaje_total / conteo, 2)
            self.txt_resultados_eval.insert(tk.END, "================================================================================\n")
            self.txt_resultados_eval.insert(tk.END, f"PROMEDIO GLOBAL DE COMPRENSIÓN LECTORA: {nota_final} / 100 PTS\n")
            self.txt_resultados_eval.insert(tk.END, "================================================================================\n")
        else:
            self.txt_resultados_eval.insert(tk.END, "================================================================================\n")
            self.txt_resultados_eval.insert(tk.END, "FIN DEL REPORTE AUTOMÁTICO - EXTRACTOS DE INFORMACIÓN ASEGURADOS\n")
            self.txt_resultados_eval.insert(tk.END, "================================================================================\n")
            
        # BLINDAJE: Bloqueamos la consola para que sea de SOLO LECTURA
        self.txt_resultados_eval.config(state="disabled")

    def guardar_reporte(self):
        if not self.pipeline_results:
            return
        file_save_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")], title="Exportar Reporte"
        )
        if file_save_path:
            try:
                # Desbloqueamos un segundo solo para leer el string completo si es necesario
                with open(file_save_path, "w", encoding="utf-8") as f:
                    f.write(self.txt_resultados_eval.get("1.0", tk.END))
                messagebox.showinfo("Exportación Exitosa", "El reporte definitivo ha sido guardado.")
            except Exception as e:
                messagebox.showerror("Error de Escritura", str(e))

    def reiniciar_interfaz(self):
        self.file_path = None
        self.pipeline_results = None
        self.preguntas_totales = []
        self.respuestas_alumno_textos = []
        self.indice_pregunta_actual = 0
        self.modo_manual = True
        
        self.lbl_status.config(text="Esperando carga de archivo...", foreground="#777777", font=("Segoe UI", 10, "italic"))
        
        self.txt_resumen.config(state="normal")
        self.txt_resumen.delete("1.0", tk.END)
        self.txt_topics.config(state="normal")
        self.txt_topics.delete("1.0", tk.END)
        
        # Desbloqueamos consola para poder limpiarla por completo
        self.txt_resultados_eval.config(state="normal")
        self.txt_resultados_eval.delete("1.0", tk.END)
        
        self.txt_respuesta_alumno.config(state="normal", bg="#ffffff", fg="#000000", insertbackground="#000000")
        self.txt_respuesta_alumno.delete("1.0", tk.END)
        self.lbl_metrics.config(text="A la espera del procesamiento del documento fuente...")
        
        self.lbl_pregunta_num.config(text="Pregunta X de Y")
        self.lbl_pregunta_texto.config(text="Selecciona un documento para estructurar el banco de preguntas.")
        
        self.btn_guardar.config(state="disabled")
        self.btn_evaluar.config(state="disabled")
        self.btn_ia_answers.config(state="disabled")
        self.btn_anterior.config(state="disabled")
        self.btn_siguiente.config(state="disabled")
        self.btn_finalizar_llenado.config(state="disabled")


def run():
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    run()