import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pymupdf as fitz 

class PDFSearchUI(ctk.CTkFrame):
    def __init__(self, master, lang="EN", **kwargs):
        super().__init__(master, **kwargs)
        self.selected_file = None
        self.current_lang = lang

        if lang == "IT":
            self.btn_select_txt = "📁  Seleziona il File PDF da Scansionare"
            self.lbl_file_txt = "Nessun file selezionato "
            self.lbl_search_txt = "Digita la parola o frase da cercare:"
            self.btn_search_txt = "🔍  AVVIA RICERCA NEL TESTO"
            self.no_results_txt = "Nessun risultato trovato per: "
            self.results_found_txt = "Trovate {count} occorrenze della parola nelle seguenti pagine:"
            self.page_txt = "Pagina"
            self.warning_select = "Seleziona prima un file PDF."
            self.warning_empty = "Inserisci una parola da cercare."
        elif lang == "DE":
            self.btn_select_txt = "📁  PDF-Datei zum Scannen auswählen"
            self.lbl_file_txt = "Keine Datei ausgewählt "
            self.lbl_search_txt = "Geben Sie das zu suchende Wort ein:"
            self.btn_search_txt = "🔍  TEXTSUCHE STARTEN"
            self.no_results_txt = "Keine Ergebnisse gefunden für: "
            self.results_found_txt = "{count} Treffer auf den folgenden Seiten gefunden:"
            self.page_txt = "Seite"
            self.warning_select = "Bitte wählen Sie zuerst eine PDF-Datei aus."
            self.warning_empty = "Bitte geben Sie ein Suchwort ein."
        elif lang == "FR":
            self.btn_select_txt = "📁  Sélectionner le fichier PDF à scanner"
            self.lbl_file_txt = "Aucun fichier sélectionné "
            self.lbl_search_txt = "Tapez le mot ou la phrase à rechercher :"
            self.btn_search_txt = "🔍  LANCER LA RECHERCHE"
            self.no_results_txt = "Aucun résultat trouvé pour : "
            self.results_found_txt = "{count} occurrences trouvées dans les pages suivantes :"
            self.page_txt = "Page"
            self.warning_select = "Veuillez d'abord sélectionner un fichier PDF."
            self.warning_empty = "Veuillez saisir un mot à rechercher."
        elif lang == "ES":
            self.btn_select_txt = "📁  Seleccionar archivo PDF para escanear"
            self.lbl_file_txt = "Ningún archivo seleccionado "
            self.lbl_search_txt = "Escriba la palabra o frase a buscar:"
            self.btn_search_txt = "🔍  INICIAR BÚSQUEDA"
            self.no_results_txt = "No se encontraron resultados para: "
            self.results_found_txt = "Se encontraron {count} ocurrencias en las siguientes páginas:"
            self.page_txt = "Página"
            self.warning_select = "Por favor, seleccione primero un archivo PDF."
            self.warning_empty = "Por favor, ingrese una palabra para buscar."
        else:
            self.btn_select_txt = "📁  Select PDF File to Scan"
            self.lbl_file_txt = "No file selected "
            self.lbl_search_txt = "Type the word or phrase to search:"
            self.btn_search_txt = "🔍  START TEXT SEARCH"
            self.no_results_txt = "No results found for: "
            self.results_found_txt = "Found {count} occurrences across the following pages:"
            self.page_txt = "Page"
            self.warning_select = "Please select a PDF file first."
            self.warning_empty = "Please enter a word to search."

        self.btn_select = ctk.CTkButton(self, text=self.btn_select_txt, command=self.select_file, height=38)
        self.btn_select.pack(fill="x", padx=20, pady=(20, 10))

        self.file_label = ctk.CTkLabel(self, text=self.lbl_file_txt, text_color="gray", font=ctk.CTkFont(size=12, slant="italic"), justify="center")
        self.file_label.pack(fill="x", padx=20, pady=(0, 15))

        self.search_frame = ctk.CTkFrame(self, fg_color="#232323")
        self.search_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.lbl_search = ctk.CTkLabel(self.search_frame, text=self.lbl_search_txt, text_color="white", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_search.pack(anchor="w", padx=20, pady=(15, 5))

        self.entry_search = ctk.CTkEntry(self.search_frame, height=35, placeholder_text="e.g. Mario Rossi, IBAN, Tax Code...")
        self.entry_search.pack(fill="x", padx=20, pady=(0, 15))

        self.btn_execute = ctk.CTkButton(self.search_frame, text=self.btn_search_txt, command=self.execute_search, font=ctk.CTkFont(size=14, weight="bold"), height=40, fg_color="#1f538d")
        self.btn_execute.pack(fill="x", padx=20, pady=(0, 15))

        self.results_box = ctk.CTkScrollableFrame(self.search_frame, fg_color="#1d1d1d", height=140)
        self.results_box.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.lbl_status = ctk.CTkLabel(self.results_box, text="", font=ctk.CTkFont(size=12))
        self.lbl_status.pack(pady=10, padx=10, anchor="w")

        self.result_widgets = []

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
        if file_path:
            self.selected_file = file_path
            self.file_label.configure(text=os.path.basename(file_path) + " ", text_color="white")
            self.clear_results()

    def execute_search(self):
        if not self.selected_file:
            messagebox.showwarning("PDFlash", self.warning_select)
            return
        
        search_term = self.entry_search.get().strip()
        if not search_term:
            messagebox.showwarning("PDFlash", self.warning_empty)
            return

        try:
            doc = fitz.open(self.selected_file)
            found_pages = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # CORRETTO: Rimossa la costante errata, impostando il flag a 0 per usare i parametri standard stabili
                text_instances = page.search_for(search_term, flags=0)
                if text_instances:
                    found_pages.append(str(page_num + 1))

            if not found_pages:
                lbl_no_res = ctk.CTkLabel(self.results_box, text=f"❌ '{search_term}': {self.no_results_txt}", text_color="#ff4444", font=ctk.CTkFont(size=12, weight="bold"))
                lbl_no_res.pack(anchor="w", padx=15, pady=2)
                self.result_widgets.append(lbl_no_res)
            else:
                pagine_str = ", ".join(found_pages)
                testo_risultato = f"🔍 {search_term}: {self.page_txt} {pagine_str}"
                
                lbl_entry = ctk.CTkLabel(self.results_box, text=testo_risultato, font=ctk.CTkFont(size=12, weight="normal"), text_color="#28a745")
                lbl_entry.pack(anchor="w", padx=15, pady=4)
                self.result_widgets.append(lbl_entry)

            self.entry_search.delete(0, "end")

        except Exception as e:
            messagebox.showerror("PDFlash", f"Error: {str(e)}")

    def clear_results(self):
        self.lbl_status.configure(text="")
        for w in self.result_widgets:
            w.destroy()
        self.result_widgets.clear()
