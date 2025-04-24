import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from helpers import procesar_pruebas
import time

# Modelos 
from models import (p1_adaii_fb, p1_adaii_vz_p3, p1_adaii_pd)

class ModCIApp(ttk.Window):
    def __init__(self):
        super().__init__(title="ModCI - Moderar Conflicto Interno", themename="journal", size=(1000, 650), resizable=(True, True))
        self.file_path = None
        self.algorithms = ["Fuerza Bruta", "Programación Dinámica", "Voraz"]
        self.test_data = None
        self.RS = None
        
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=X, padx=10, pady=(10, 0))
        title_label = ttk.Label(
            title_frame, 
            text="Moderando el conflicto interno de opiniones en una red social (MCI)", 
            font=("TkDefaultFont", 16, "bold"),
            bootstyle=PRIMARY
        )
        title_label.pack(anchor=CENTER)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.tab_single = ttk.Frame(notebook)
        self.tab_compare = ttk.Frame(notebook)
        notebook.add(self.tab_single, text="Ejecutar algoritmo")
        notebook.add(self.tab_compare, text="Comparar algoritmos")

        self.setup_single_tab()
        self.setup_compare_tab()

    def setup_single_tab(self):
        # Crear un frame principal que contendrá todo
        main_frame = ttk.Frame(self.tab_single)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Dividir en dos columnas
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        right_frame = ttk.LabelFrame(main_frame, text="Información de la prueba", padding=10)
        right_frame.pack(side=RIGHT, fill=Y, expand=False, padx=(10, 0))
        
        
        # Contenido del frame izquierdo (como estaba antes)
        frame = ttk.Labelframe(left_frame, text="Ejecutar algoritmo", padding=10)
        frame.pack(fill=BOTH, expand=True)

        # Selector de archivo
        ttk.Label(frame, text="Archivo de entrada:").pack(anchor=W)
        ttk.Button(frame, text="Seleccionar archivo", command=self.seleccionar_archivo).pack(anchor=W, pady=5)
        self.label_archivo = ttk.Label(frame, text="Ningún archivo seleccionado", bootstyle=INFO)
        self.label_archivo.pack(anchor=W)

        # Dropdown de algoritmo
        ttk.Label(frame, text="Selecciona un algoritmo:").pack(anchor=W, pady=(15, 0))
        self.alg_var = ttk.StringVar(value=self.algorithms[0])
        ttk.Combobox(frame, textvariable=self.alg_var, values=self.algorithms, state="readonly").pack(anchor=W, pady=5)

        # Botón procesar
        ttk.Button(frame, text="Procesar", command=self.procesar_algoritmo, bootstyle=SUCCESS).pack(anchor=W, pady=10)

        # TextArea para mostrar resultados
        self.resultado_text = ttk.Text(frame, height=12)
        self.resultado_text.pack(fill=BOTH, expand=True, pady=10)
        
        # Configuración del panel derecho (información de la prueba)
        self.test_info_text = ttk.Text(right_frame, width=45, height=20)
        self.test_info_text.pack(fill=BOTH, expand=True)

    def setup_compare_tab(self):
        main_frame = ttk.Frame(self.tab_compare)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior para la configuración y botones
        top_frame = ttk.LabelFrame(main_frame, text="Comparar algoritmos", padding=10)
        top_frame.pack(fill=X, expand=False, pady=(0, 10))
        
        # Cargar prueba
        file_frame = ttk.Frame(top_frame)
        file_frame.pack(fill=X, pady=(0, 10))
        ttk.Button(file_frame, text="Seleccionar archivo de prueba", 
                   command=self.seleccionar_archivo_comparar).pack(side=LEFT, padx=10)
        self.label_archivo_comparar = ttk.Label(file_frame, text="Ningún archivo seleccionado", bootstyle=INFO)
        self.label_archivo_comparar.pack(side=LEFT, fill=X, expand=True)

        # Frame para los algoritmos
        alg_frame = ttk.Frame(top_frame)
        alg_frame.pack(fill=X, expand=False)
        
        # Selección de algoritmos
        left_frame = ttk.Frame(alg_frame)
        left_frame.pack(side=LEFT, fill=X, expand=True)

        right_frame = ttk.Frame(alg_frame)
        right_frame.pack(side=LEFT, fill=X, expand=True)

        ttk.Label(left_frame, text="Algoritmo 1:").pack(anchor=W)
        self.alg1_var = ttk.StringVar(value=self.algorithms[0])
        ttk.Combobox(left_frame, textvariable=self.alg1_var, values=self.algorithms, state="readonly").pack(fill=X, pady=5, padx=10)

        ttk.Label(right_frame, text="Algoritmo 2:").pack(anchor=W)
        self.alg2_var = ttk.StringVar(value=self.algorithms[1])
        ttk.Combobox(right_frame, textvariable=self.alg2_var, values=self.algorithms, state="readonly").pack(fill=X, pady=5, padx=10)

        # Botón comparar
        ttk.Button(top_frame, text="Comparar", command=self.comparar_algoritmos, bootstyle=PRIMARY).pack(pady=10)

        # Frame para el contenido inferior (gráfico e información)
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=BOTH, expand=True)
        
        # Frame para el gráfico
        graph_frame = ttk.LabelFrame(bottom_frame, text="Resultados gráficos", padding=10)
        graph_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Gráfica
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Frame para la información de la prueba y resultados
        info_frame = ttk.LabelFrame(bottom_frame, text="Información", padding=10, width=300)
        info_frame.pack(side=RIGHT, fill=BOTH, expand=False, padx=(10, 0), pady=0)
        
        # Crear un notebook para tener pestañas en el panel de información
        info_notebook = ttk.Notebook(info_frame)
        info_notebook.pack(fill=BOTH, expand=True)
        
        # Pestaña de información de la prueba
        test_info_tab = ttk.Frame(info_notebook)
        info_notebook.add(test_info_tab, text="Datos de prueba")
        
        self.test_info_text_compare = ttk.Text(test_info_tab, width=45, height=20)
        self.test_info_text_compare.pack(fill=BOTH, expand=True)
        
        # Pestaña de comparación de resultados
        results_tab = ttk.Frame(info_notebook)
        info_notebook.add(results_tab, text="Resultados")
        
        self.comparison_results_text = ttk.Text(results_tab, width=45, height=20)
        self.comparison_results_text.pack(fill=BOTH, expand=True)

    def seleccionar_archivo(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if path:
            self.file_path = path
            self.label_archivo.config(text=path)
            self.cargar_test_data(path)
            self.RS = procesar_pruebas.procesar_pruebas(self.file_path)
            self.mostrar_test_info()

    def seleccionar_archivo_comparar(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if path:
            self.file_path = path
            self.label_archivo_comparar.config(text=path)
            self.cargar_test_data(path)
            self.RS = procesar_pruebas.procesar_pruebas(self.file_path)
            self.mostrar_test_info_compare()

    def cargar_test_data(self, path):
        try:
            with open(path, 'r') as file:
                lineas = list(map(lambda x: x.strip(), file.readlines()))

                n = int(lineas[0])
                lineas.pop(0)

                grupos_agentes = []
                for i in range(n):
                    if i < len(lineas):
                        line = lineas[i]
                        partes = line.split(',')
                        if len(partes) >= 4:
                            grupo = {
                                'n_agentes': int(partes[0]),
                                'opinion1': int(partes[1]),
                                'opinion2': int(partes[2]),
                                'rigidez': float(partes[3])
                            }
                            grupos_agentes.append(grupo)

                r_max = int(lineas[n]) if n < len(lineas) else 0

                self.test_data = {
                    'n': n,
                    'grupos': grupos_agentes,
                    'r_max': r_max
                }

                # Calcular combinaciones posibles para información
                combinaciones_posibles = 1
                for grupo in grupos_agentes:
                    combinaciones_posibles *= grupo['n_agentes'] + 1

                self.test_data['combinaciones'] = combinaciones_posibles

        except Exception as e:
                messagebox.showerror("Error", f"Error al cargar los datos: {str(e)}")
                self.test_data = None
    
    def mostrar_test_info(self):
        if self.test_data:
            self.test_info_text.delete(1.0, 'end')

            self.test_info_text.insert('end', f"Número de grupos: {self.test_data['n']}\n")
            self.test_info_text.insert('end', f"Valor máximo (R_max): {self.test_data['r_max']}\n")
            self.test_info_text.insert('end', f"Combinaciones posibles: {self.test_data['combinaciones']}\n\n")

            self.test_info_text.insert('end', "Grupos de agentes:\n")
            for i, grupo in enumerate(self.test_data['grupos'][:20]):  # Mostrar solo los primeros 10 grupos
                self.test_info_text.insert('end', f"  {i+1}. Agentes: {grupo['n_agentes']}, ")
                self.test_info_text.insert('end', f"Op1: {grupo['opinion1']}, ")
                self.test_info_text.insert('end', f"Op2: {grupo['opinion2']}, ")
                self.test_info_text.insert('end', f"Rigidez: {grupo['rigidez']}\n")

            if len(self.test_data['grupos']) > 10:
                self.test_info_text.insert('end', f"\n... y {len(self.test_data['grupos']) - 10} grupos más\n")

    def mostrar_test_info_compare(self):
        if self.test_data:
            self.test_info_text_compare.delete(1.0, 'end')

            self.test_info_text_compare.insert('end', f"Número de grupos: {self.test_data['n']}\n")
            self.test_info_text_compare.insert('end', f"Valor máximo (R_max): {self.test_data['r_max']}\n")
            self.test_info_text_compare.insert('end', f"Combinaciones posibles: {self.test_data['combinaciones']}\n\n")

            self.test_info_text_compare.insert('end', "Grupos de agentes:\n")
            for i, grupo in enumerate(self.test_data['grupos'][:20]):  # Mostrar solo los primeros 10 grupos
                self.test_info_text_compare.insert('end', f"  {i+1}. Agentes: {grupo['n_agentes']}, ")
                self.test_info_text_compare.insert('end', f"Op1: {grupo['opinion1']}, ")
                self.test_info_text_compare.insert('end', f"Op2: {grupo['opinion2']}, ")
                self.test_info_text_compare.insert('end', f"Rigidez: {grupo['rigidez']}\n")

            if len(self.test_data['grupos']) > 10:
                self.test_info_text_compare.insert('end', f"\n... y {len(self.test_data['grupos']) - 10} grupos más\n")

    def procesar_algoritmo(self):
        alg = self.alg_var.get()
        if not self.file_path and not self.RS:
            messagebox.showerror("Error", "Selecciona un archivo.")
            return

        resultado = f""
        
        solucion, valor_solucion, esfuerzo_final = self.ejecutar_algoritmo(alg)
        
        resultado += f"{alg.upper()}".center(100, "-")
        resultado += f"\nEstrategia: {solucion}\n"
        grupos_dict = self.test_data['grupos']
        resultado += "\nRed modificada:\n"
        for i, grupo in enumerate(grupos_dict):
            agentes_orig = grupo['n_agentes']
            agentes_mod = agentes_orig - solucion[i]
            if agentes_mod > 0:
                linea = (
                    f"  {i+1}. Agentes: {agentes_mod}, "
                    f"Op1: {grupo['opinion1']}, Op2: {grupo['opinion2']}, "
                    f"Rigidez: {grupo['rigidez']:.3f}\n"
                )
                resultado += f"{linea}\n"
        resultado += f"Conflicto: {valor_solucion}"
        resultado += f"\nEsfuerzo: {esfuerzo_final}"
            
            
        self.resultado_text.delete(1.0, 'end')
        self.resultado_text.insert('end', resultado)

    def ejecutar_algoritmo(self, nombre_algoritmo):
        if nombre_algoritmo == "Voraz":
            return p1_adaii_vz_p3.ModCI_voraz(self.RS)
        elif nombre_algoritmo == "Fuerza Bruta":
            return p1_adaii_fb.ModCI_fb(self.RS)
        elif nombre_algoritmo == "Programación Dinámica":
            print(self.RS)
            return p1_adaii_pd.ModCI_pd(self.RS)
        else:
            return None

    def comparar_algoritmos(self):
        if not self.file_path or not self.RS:
            messagebox.showerror("Error", "Selecciona un archivo primero.")
            return
        
        # Obtener los algoritmos seleccionados
        alg1 = self.alg1_var.get()
        alg2 = self.alg2_var.get()
        
        if alg1 == alg2:
            messagebox.showwarning("Advertencia", "Por favor selecciona dos algoritmos diferentes para comparar.")
            return
        
        inicio_tiempo1 = time.time()
        resultado1 = self.ejecutar_algoritmo(alg1)
        tiempo1 = time.time() - inicio_tiempo1
        inicio_tiempo2 = time.time()
        resultado2 = self.ejecutar_algoritmo(alg2)
        tiempo2 = time.time() - inicio_tiempo2

        if not resultado1 or not resultado2:
            messagebox.showerror("Error", "Error al ejecutar los algoritmos.")
            return
        
        # Desempaquetar resultados
        estrategia1, conflicto1, esfuerzo1 = resultado1
        estrategia2, conflicto2, esfuerzo2 = resultado2
        
        # Limpiar gráfico anterior
        self.ax.clear()
        
        # Crear datos para el histograma de barras
        n_grupos = len(estrategia1)
        ind = np.arange(n_grupos)
        width = 0.4
        
        # Crear barras para los dos algoritmos
        rects1 = self.ax.bar(ind - width/2, estrategia1, width, label=alg1)
        rects2 = self.ax.bar(ind + width/2, estrategia2, width, label=alg2)
        
        # Personalizar gráfico
        self.ax.set_xlabel('Grupos')
        self.ax.set_ylabel('Número de agentes')
        self.ax.set_title(f'Comparación de estrategias: {alg1} vs {alg2}')
        self.ax.set_xticks(ind)
        self.ax.set_xticklabels([str(i+1) for i in range(n_grupos)])
        self.ax.legend()
        # Hacer el gráfico más responsivo si se redimensiona la ventana
        self.ax.set_ylim(0, max(max(estrategia1), max(estrategia2)) * 1.1)  # Ajustar el límite superior del eje y
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Mostrar valores sobre las barras
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                self.ax.annotate(f'{height}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                            textcoords="offset points",
                            ha='center', va='bottom')
        
        autolabel(rects1)
        autolabel(rects2)
        
        # Actualizar el gráfico
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Mostrar resultados en el área de texto
        self.comparison_results_text.delete(1.0, 'end')
        
        porcentaje_error = None
        referencia = None
        if alg1 == "Voraz" and (alg2 == "Programación Dinámica" or alg2 == "Fuerza Bruta"):
            referencia = alg2 
            porcentaje_error = 1 - (conflicto2/conflicto1) if conflicto1 > 0 else 0
        elif alg2 == "Voraz" and (alg1 == "Programación Dinámica" or alg1 == "Fuerza Bruta"):
            referencia = alg1
            porcentaje_error = 1 - (conflicto1/conflicto2) if conflicto2 > 0 else 0
        
        self.comparison_results_text.insert('end', f"{alg1}:\n")
        self.comparison_results_text.insert('end', f"  Estrategia: {estrategia1}\n")
        grupos_dict = self.test_data['grupos']
        self.comparison_results_text.insert('end', "\nRed modificada:\n")
        for i, grupo in enumerate(grupos_dict):
            agentes_orig = grupo['n_agentes']
            agentes_mod = agentes_orig - estrategia1[i]
            if agentes_mod > 0:
                linea = (
                    f"  {i+1}. Agentes: {agentes_mod}, "
                    f"Op1: {grupo['opinion1']}, Op2: {grupo['opinion2']}, "
                    f"Rigidez: {grupo['rigidez']:.3f}\n"
                )
                self.comparison_results_text.insert('end', f"{linea}\n")
        self.comparison_results_text.insert('end', f"  Conflicto: {conflicto1:.6f}\n")
        self.comparison_results_text.insert('end', f"  Esfuerzo: {esfuerzo1}\n")
        self.comparison_results_text.insert('end', f"  Tiempo de ejecución: {tiempo1:.6f} segundos\n\n")
        
        self.comparison_results_text.insert('end', f"{alg2}:\n")
        self.comparison_results_text.insert('end', f"  Estrategia: {estrategia2}\n")
        grupos_dict = self.test_data['grupos']
        self.comparison_results_text.insert('end', "\nRed modificada:\n")
        for i, grupo in enumerate(grupos_dict):
            agentes_orig = grupo['n_agentes']
            agentes_mod = agentes_orig - estrategia2[i]
            if agentes_mod > 0:
                linea = (
                    f"  {i+1}. Agentes: {agentes_mod}, "
                    f"Op1: {grupo['opinion1']}, Op2: {grupo['opinion2']}, "
                    f"Rigidez: {grupo['rigidez']:.3f}\n"
                )
                self.comparison_results_text.insert('end', f"{linea}\n")
        self.comparison_results_text.insert('end', f"  Conflicto: {conflicto2:.6f}\n")
        self.comparison_results_text.insert('end', f"  Esfuerzo: {esfuerzo2}\n")
        self.comparison_results_text.insert('end', f"  Tiempo de ejecución: {tiempo2:.6f} segundos\n\n")
        
        self.comparison_results_text.insert('end', f"Diferencias:\n")
        self.comparison_results_text.insert('end', f"  Conflicto: {abs(conflicto1 - conflicto2):.6f}\n")
        self.comparison_results_text.insert('end', f"  Esfuerzo: {abs(esfuerzo1 - esfuerzo2)}\n")
        
        if porcentaje_error is not None:
            self.comparison_results_text.insert('end', f"\nPorcentaje de error (Voraz vs {referencia}):\n")
            self.comparison_results_text.insert('end', f"  {porcentaje_error:.2f}%\n")
            

if __name__ == "__main__":
    app = ModCIApp()
    app.mainloop()