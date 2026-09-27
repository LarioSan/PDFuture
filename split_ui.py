import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter

class PDFSplitterUI(ctk.CTkFrame):
    def __init__(self, master, lang_dict=None, lang="EN", **kwargs):
        super().__init__(master, **kwargs)
        self.selected_file = None
        self.mode = ctk.StringVar(value="range") 

        # FIX GRAFICO: Aggiunto uno spazio vuoto alla fine di ogni stringa per proteggere il corsivo dai tagli
        if lang == "IT":
            self.btn_txt = "📁  Seleziona il File PDF da Dividere"
            self.lbl_file = "Nessun file selezionato "
            self.title_txt = "Scegli la modalità di divisione:"
            self.r1_txt = "Estrai un intervallo di pagine specifico"
            self.r2_txt = "Separa OGNI singola pagina in file distinti"
            self.from_txt = "Da pagina:"
            self.to_txt = "A pagina:"
            self.exec_txt = "✂️  DIVIDI E SALVA PDF"
        elif lang == "DE":
            self.btn_txt = "📁  PDF-Datei zum Teilen auswählen"
            self.lbl_file = "Keine Datei ausgewählt "
            self.title_txt = "Wählen Sie den Teilungsmodus:"
            self.r1_txt = "Bestimmten Seitenbereich extrahieren"
            self.r2_txt = "JEDE einzelne Seite in separate Dateien aufteilen"
            self.from_txt = "Von Seite:"
            self.to_txt = "Bis Seite:"
            self.exec_txt = "✂️  PDF TEILEN UND SPEICHERN"
        elif lang == "FR":
            self.btn_txt = "📁  Sélectionner le fichier PDF à diviser"
            self.lbl_file = "Aucun fichier sélectionné "
            self.title_txt = "Choisissez le mode de division :"
            self.r1_txt = "Extraire un intervalle de pages spécifique"
            self.r2_txt = "Séparer CHAQUE page en fichiers distincts"
            self.from_txt = "De la page :"
            self.to_txt = "À la page :"
            self.exec_txt = "✂️  DIVISER ET ENREGISTRER LE PDF"
        elif lang == "ES":
            self.btn_txt = "📁  Seleccionar archivo PDF para dividir"
            self.lbl_file = "Ningún archivo seleccionado "
            self.title_txt = "Elija el modo de división:"
            self.r1_txt = "Extraer un intervalo de páginas específico"
            self.r2_txt = "Separar CADA página en archivos independientes"
            self.from_txt = "De página:"
            self.to_txt = "A página:"
            self.exec_txt = "✂️  DIVIDIR Y GUARDAR PDF"
        else:
            self.btn_txt = "📁  Select PDF File to Split"
            self.lbl_file = "No file selected "
            self.title_txt = "Choose splitting mode:"
            self.r1_txt = "Extract a specific page range"
            self.r2_txt = "Separate EVERY single page into distinct files"
            self.from_txt = "From page:"
            self.to_txt = "To page:"
            self.exec_txt = "✂️  SPLIT AND SAVE PDF"

        self.btn_select = ctk.CTkButton(self, text=self.btn_txt, command=self.select_file, height=38)
        self.btn_select.pack(fill="x", padx=20, pady=(20, 10))

        self.file_label = ctk.CTkLabel(self, text=self.lbl_file, text_color="gray", font=ctk.CTkFont(size=12, slant="italic"), justify="center")
        self.file_label.pack(fill="x", padx=20, pady=(0, 20))

        self.options_frame = ctk.CTkFrame(self, fg_color="#232323")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.options_title = ctk.CTkLabel(self.options_frame, text=self.title_txt, text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
        self.options_title.pack(anchor="w", padx=15, pady=15)

        self.radio_range = ctk.CTkRadioButton(self.options_frame, text=self.r1_txt, text_color="white", variable=self.mode, value="range", command=self.toggle_inputs)
        self.radio_range.pack(anchor="w", padx=20, pady=5)

        self.inputs_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.inputs_frame.pack(anchor="w", padx=45, pady=(5, 15))

        self.lbl_from = ctk.CTkLabel(self.inputs_frame, text=self.from_txt, text_color="white")
        self.lbl_from.pack(side="left", padx=(0, 5))
        self.entry_from = ctk.CTkEntry(self.inputs_frame, width=50, justify="center")
        self.entry_from.insert(0, "1")
        self.entry_from.pack(side="left", padx=(0, 15))

        self.lbl_to = ctk.CTkLabel(self.inputs_frame, text=self.to_txt, text_color="white")
        self.lbl_to.pack(side="left", padx=(0, 5))
        self.entry_to = ctk.CTkEntry(self.inputs_frame, width=50, justify="center")
        self.entry_to.insert(0, "1")
        self.entry_to.pack(side="left")

        self.radio_all = ctk.CTkRadioButton(self.options_frame, text=self.r2_txt, text_color="white", variable=self.mode, value="all", command=self.toggle_inputs)
        self.radio_all.pack(anchor="w", padx=20, pady=5)

        self.btn_execute = ctk.CTkButton(self, text=self.exec_txt, command=self.execute_split, font=ctk.CTkFont(size=14, weight="bold"), height=45, fg_color="#218838", hover_color="#28a745")
        self.btn_execute.pack(fill="x", padx=20, pady=(0, 20))

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
        if file_path:
            self.selected_file = file_path
            # Appende lo spazio di sicurezza anche al nome del file caricato dinamicamente
            self.file_label.configure(text=os.path.basename(file_path) + " ")
            try:
                reader = PdfReader(file_path)
                total_pages = len(reader.pages)
                self.entry_to.delete(0, "end")
                self.entry_to.insert(0, str(total_pages))
            except Exception:
                pass

    def toggle_inputs(self):
        if self.mode.get() == "all":
            self.entry_from.configure(state="disabled", fg_color="#333333")
            self.entry_to.configure(state="disabled", fg_color="#333333")
        else:
            self.entry_from.configure(state="normal", fg_color="#1d1d1d")
            self.entry_to.configure(state="normal", fg_color="#1d1d1d")

    def execute_split(self):
        if not self.selected_file:
            messagebox.showwarning("PDFlash", "No file selected.")
            return
        try:
            reader = PdfReader(self.selected_file)
            total_pages = len(reader.pages)

            if self.mode.get() == "range":
                try:
                    start_page = int(self.entry_from.get())
                    end_page = int(self.entry_to.get())
                except ValueError:
                    messagebox.showerror("PDFlash", "Invalid page numbers.")
                    return
                if start_page < 1 or end_page > total_pages or start_page > end_page:
                    messagebox.showerror("PDFlash", "Invalid range.")
                    return
                output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("File PDF", "*.pdf")])
                if output_path:
                    writer = PdfWriter()
                    for page_num in range(start_page - 1, end_page):
                        writer.add_page(reader.pages[page_num])
                    with open(output_path, "wb") as f:
                        writer.write(f)
                    messagebox.showinfo("PDFlash", "Success!")
            else:
                output_dir = filedialog.askdirectory()
                if output_dir:
                    base_name = os.path.splitext(os.path.basename(self.selected_file))
                    for page_num in range(total_pages):
                        writer = PdfWriter()
                        writer.add_page(reader.pages[page_num])
                        output_path = os.path.join(output_dir, f"{base_name}_page_{page_num + 1}.pdf")
                        with open(output_path, "wb") as f:
                            writer.write(f)
                    messagebox.showinfo("PDFlash", "Success!")
        except Exception as e:
            messagebox.showerror("PDFlash", str(e))
