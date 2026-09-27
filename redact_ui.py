import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pymupdf as fitz 

class PDFRedactUI(ctk.CTkFrame):
    def __init__(self, master, lang="EN", **kwargs):
        super().__init__(master, **kwargs)
        self.selected_file = None

        if lang == "IT":
            self.btn_select_txt = "📁  Seleziona il File PDF da Censurare"
            self.lbl_file_txt = "Nessun file selezionato "
            self.lbl_input_txt = "Digita il testo sensibile da eliminare per sempre:"
            self.btn_exec_txt = "🖤  AVVIA OSCURAMENTO PERMANENTE"
            self.warning_select = "Seleziona prima un file PDF."
            self.warning_empty = "Inserisci il testo da censurare."
            self.success_txt = "Censura completata! Trovate e distrutte {count} occorrenze."
        elif lang == "DE":
            self.btn_select_txt = "📁  PDF-Datei zum Schwärzen auswählen"
            self.lbl_file_txt = "Keine Datei ausgewählt "
            self.lbl_input_txt = "Geben Sie den Text ein, der dauerhaft gelöscht werden soll:"
            self.btn_exec_txt = "🖤  DAUERHAFTE SCHWÄRZUNG STARTEN"
            self.warning_select = "Bitte wählen Sie zuerst eine PDF-Datei aus."
            self.warning_empty = "Bitte geben Sie den zu schwärzenden Text ein."
            self.success_txt = "Schwärzung abgeschlossen! {count} Vorkommen gelöscht."
        elif lang == "FR":
            self.btn_select_txt = "📁  Sélectionner le fichier PDF à masquer"
            self.lbl_file_txt = "Aucun fichier sélectionné "
            self.lbl_input_txt = "Saisissez le texte sensible à supprimer définitivement :"
            self.btn_exec_txt = "🖤  LANCER LE MASQUAGE PERMANENT"
            self.warning_select = "Veuillez d'abord sélectionner un fichier PDF."
            self.warning_empty = "Veuillez saisir le texte à masquer."
            self.success_txt = "Masquage réussi ! {count} occurrences détruites."
        elif lang == "ES":
            self.btn_select_txt = "📁  Seleccionar archivo PDF para ocultar"
            self.lbl_file_txt = "Ningún archivo seleccionado "
            self.lbl_input_txt = "Escriba el texto confidencial a eliminar para siempre:"
            self.btn_exec_txt = "🖤  INICIAR OCULTACIÓN PERMANENTE"
            self.warning_select = "Por favor, seleccione primero un archivo PDF."
            self.warning_empty = "Por favor, ingrese el texto a ocultar."
            self.success_txt = "¡Ocultación completada! {count} ocurrencias destruidas."
        else:
            self.btn_select_txt = "📁  Select PDF File to Redact"
            self.lbl_file_txt = "No file selected "
            self.lbl_input_txt = "Type sensitive text to delete permanently:"
            self.btn_exec_txt = "🖤  START PERMANENT REDACTION"
            self.warning_select = "Please select a PDF file first."
            self.warning_empty = "Please enter text to redact."
            self.success_txt = "Redaction complete! {count} instances destroyed."

        self.btn_select = ctk.CTkButton(self, text=self.btn_select_txt, command=self.select_file, height=38)
        self.btn_select.pack(fill="x", padx=20, pady=(20, 10))

        self.file_label = ctk.CTkLabel(self, text=self.lbl_file_txt, text_color="gray", font=ctk.CTkFont(size=12, slant="italic"), justify="center")
        self.file_label.pack(fill="x", padx=20, pady=(0, 15))

        self.redact_frame = ctk.CTkFrame(self, fg_color="#232323")
        self.redact_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.lbl_input = ctk.CTkLabel(self.redact_frame, text=self.lbl_input_txt, text_color="white", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_input.pack(anchor="w", padx=20, pady=(15, 5))

        self.entry_redact = ctk.CTkEntry(self.redact_frame, height=35, placeholder_text="e.g. SecretPassword, IBAN, ClientName...")
        self.entry_redact.pack(fill="x", padx=20, pady=(0, 20))

        self.btn_execute = ctk.CTkButton(self, text=self.btn_exec_txt, command=self.execute_redaction, font=ctk.CTkFont(size=14, weight="bold"), height=45, fg_color="#6e1a1a", hover_color="#8a2323", text_color="white")
        self.btn_execute.pack(fill="x", padx=20, pady=(0, 20))

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
        if file_path:
            self.selected_file = file_path
            self.file_label.configure(text=os.path.basename(file_path) + " ", text_color="white")

    def execute_redaction(self):
        if not self.selected_file:
            messagebox.showwarning("PDFlash", self.warning_select)
            return

        raw_input = self.entry_redact.get().strip()
        if not raw_input:
            messagebox.showwarning("PDFlash", self.warning_empty)
            return

        # Separa le parole inserite tramite virgola e pulisce gli spazi prima e dopo il testo (.strip())
        parole_da_censurare = [p.strip() for p in raw_input.split(",") if p.strip()]

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("File PDF", "*.pdf")])
        if output_path:
            try:
                doc = fitz.open(self.selected_file)
                total_counter = 0

                for page in doc:
                    ha_censurato_in_pagina = False
                    
                    for termine in parole_da_censurare:
                        # CORRETTO: Impostati i flag di tolleranza nativi corretti di PyMuPDF (0 = ricerca standard flessibile)
                        rects = page.search_for(termine, flags=0)
                        
                        for rect in rects:
                            if hasattr(page, "add_redact_annotation"):
                                page.add_redact_annotation(rect, fill=(0, 0, 0))
                            else:
                                page.add_redact_annot(rect, fill=(0, 0, 0))
                            total_counter += 1
                            ha_censurato_in_pagina = True
                    
                    if ha_censurato_in_pagina:
                        if hasattr(page, "apply_redactions"):
                            page.apply_redactions(images=1, graphics=1, text=1)
                        else:
                            page.apply_redactions()

                doc.save(output_path, garbage=4, deflate=True)
                doc.close()

                messagebox.showinfo("PDFlash", self.success_txt.format(count=total_counter))
                self.selected_file = None
                self.file_label.configure(text=self.lbl_file_txt, text_color="gray")
                self.entry_redact.delete(0, "end")
            except Exception as e:
                messagebox.showerror("PDFlash", f"Error: {str(e)}")
