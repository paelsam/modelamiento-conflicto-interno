import tkinter as tk
from tkinter import filedialog, messagebox
from helpers.procesar_pruebas import procesar_pruebas
from models.p1_adaii_fb import ModCI_fb

class ModCIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Moderar el conflicto interno de opiniones en una red social (ModCI)")
        self.root.geometry("800x500")

  
        self.title_label = tk.Label(root, text="Moderar el conflicto interno de opiniones en una red social (ModCI)", font=("Arial", 16, "bold"), fg="green")
        self.title_label.pack(pady=10)

      
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

     
        self.file_label = tk.Label(self.top_frame, text="Selecciona el archivo de entrada (formato .txt):")
        self.file_label.grid(row=0, column=0, padx=5, sticky="w")

        self.select_button = tk.Button(self.top_frame, text="Seleccionar archivo", command=self.seleccionar_archivo)
        self.select_button.grid(row=0, column=1, padx=5)

        self.selected_file_label = tk.Label(self.top_frame, text="Ningún archivo seleccionado")
        self.selected_file_label.grid(row=0, column=2, padx=5, sticky="w")


        self.solution_label = tk.Label(self.top_frame, text="Selecciona la solución:")
        self.solution_label.grid(row=0, column=3, padx=5, sticky="w")

        self.solution_var = tk.StringVar()
        self.solution_dropdown = tk.OptionMenu(self.top_frame, self.solution_var, "Fuerza Bruta")
        self.solution_dropdown = tk.OptionMenu(self.top_frame, self.solution_var, "Programación Dinámica")
        self.solution_dropdown.grid(row=0, column=4, padx=5)


        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.process_button = tk.Button(self.button_frame, text="Procesar", bg="green", fg="white", command=self.procesar)
        self.process_button.grid(row=0, column=0, padx=5)

        self.download_button = tk.Button(self.button_frame, text="Descargar Resultado", bg="green", fg="white", command=self.guardar_resultado, state="disabled")
        self.download_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Limpiar", bg="red", fg="white", command=self.limpiar)
        self.clear_button.grid(row=0, column=2, padx=5)

 
        self.result_label = tk.Label(root, text="Resultados:")
        self.result_label.pack(pady=5, anchor="w")

        self.result_text = tk.Text(root, height=15, width=80)
        self.result_text.pack(pady=5)


        self.file_path = None

    def seleccionar_archivo(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if self.file_path:
            self.selected_file_label.config(text=self.file_path)

    def procesar(self):
        if not self.file_path:
            messagebox.showerror("Error", "Por favor, selecciona un archivo de entrada.")
            return
        
        try:
            red_social = procesar_pruebas(self.file_path)
            conflicto, esfuerzo, estrategia = ModCI_fb(red_social)

        
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Conflicto interno: {conflicto}\n")
            self.result_text.insert(tk.END, f"Esfuerzo: {esfuerzo}\n")
            self.result_text.insert(tk.END, f"Estrategia: {estrategia}\n")

            self.download_button.config(state="normal")  

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo: {e}")

    def guardar_resultado(self):
        archivo_salida = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Archivos de texto", "*.txt")])
        if archivo_salida:
            try:
                with open(archivo_salida, 'w') as archivo:
                    archivo.write(self.result_text.get(1.0, tk.END))
                messagebox.showinfo("Éxito", "Resultados guardados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

    def limpiar(self):
        self.result_text.delete(1.0, tk.END)
        self.selected_file_label.config(text="Ningún archivo seleccionado")
        self.download_button.config(state="disabled")
        self.file_path = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ModCIGUI(root)
    root.mainloop()