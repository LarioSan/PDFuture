import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter

class PDFCompressorUI(ctk.CTkFrame):
    def __init__(self, master, lang="EN", **kwargs):
        super().__init__(master, **kwargs)
        self.selected_file = None

        # Configurazione del dizionario linguistico interno al modulo
        if lang == "IT":
            self.btn_select_txt = "📁  Seleziona il File PDF da Comprimere"
            self.lbl_file_txt = "Nessun file selezionato "
            self.info_box_txt = "⚙️  Ottimizzazione Strutturale Offline:\n\n- Riduce la dimensione dei flussi di dati interni.\n- Rimuove metadati e font duplicati inutilizzati.\n- Ideale per sbloccare l'invio su portali INPS ed Entrate."
            self.btn_exec_txt = "⚡  AVVIA COMPRESSIONE INTELLIGENTE"
            self.warning_select = "Seleziona prima un file PDF."
            self.success_txt = "Compressione completata!\n\nDimensione originale: {orig:.2f} MB\nNuova dimensione: {comp:.2f} MB"
        elif lang == "DE":
            self.btn_select_txt = "📁  PDF-Datei zum Komprimieren auswählen"
            self.lbl_file_txt = "Keine Datei ausgewählt "
            self.info_box_txt = "⚙️  Strukturelle Offline-Optimierung:\n\n- Reduziert die Größe interner Datenströme.\n- Entfernt ungenutzte doppelte Metadaten und Schriftarten.\n- Ideal für Uploads auf Behördenportale."
            self.btn_exec_txt = "⚡  INTELLIGENTE KOMPRIMIERUNG STARTEN"
            self.warning_select = "Bitte wählen Sie zuerst eine PDF-Datei aus."
            self.success_txt = "Komprimierung abgeschlossen!\n\nOriginalgröße: {orig:.2f} MB\nNeue Größe: {comp:.2f} MB"
        elif lang == "FR":
            self.btn_select_txt = "📁  Sélectionner le fichier PDF à compresser"
            self.lbl_file_txt = "Aucun fichier sélectionné "
            self.info_box_txt = "⚙️  Optimisation structurelle hors ligne:\n\n- Réduit la taille des flux de données internes.\n- Supprime les métadonnées et polices dupliquées inutilisées.\n- Idéal pour les téléversements sur les portails officiels."
            self.btn_exec_txt = "⚡  LANCER LA COMPRESSION INTELLIGENTE"
            self.warning_select = "Veuillez d'abord sélectionner un fichier PDF."
            self.success_txt = "Compression réussie !\n\nTaille originale: {orig:.2f} MB\nNouvelle taille: {comp:.2f} MB"
        elif lang == "ES":
            self.btn_select_txt = "📁  Seleccionar archivo PDF para comprimir"
            self.lbl_file_txt = "Ningún archivo seleccionado "
            self.info_box_txt = "⚙️  Optimización estructural fuera de línea:\n\n- Reduce el tamaño de los flujos de datos internos.\n- Elimina metadatos y fuentes duplicadas no utilizadas.\n- Ideal para subidas en portales gubernamentales."
            self.btn_exec_txt = "⚡  INICIAR COMPRESIÓN INTELIGENTE"
            self.warning_select = "Por favor, seleccione primero un archivo PDF."
            self.success_txt = "¡Compresión completada!\n\nTamaño original: {orig:.2f} MB\nTamaño nuevo: {comp:.2f} MB"
        else:
            self.btn_select_txt = "📁  Select PDF File to Compress"
            self.lbl_file_txt = "No file selected "
            self.info_box_txt = "⚙️  Offline Structural Optimization:\n\n- Reduces the size of internal data streams.\n- Removes unused duplicate metadata and embedded fonts.\n- Ideal for official or government portal uploads."
            self.btn_exec_txt = "⚡  START SMART COMPRESSION"
            self.warning_select = "Please select a PDF file first."
            self.success_txt = "Compression complete!\n\nOriginal size: {orig:.2f} MB\nNew size: {comp:.2f} MB"

        # Interfaccia Grafica Minimal Premium (Coordinata con i fix dei colori chiari)
        self.btn_select = ctk.CTkButton(self, text=self.btn_select_txt, command=self.select_file, height=38)
        self.btn_select.pack(fill="x", padx=20, pady=(20, 10))

        # Testo descrittivo in grigio opaco con spazio di sicurezza anti-taglio
        self.file_label = ctk.CTkLabel(self, text=self.lbl_file_txt, text_color="gray", font=ctk.CTkFont(size=12, slant="italic"), justify="center")
        self.file_label.pack(fill="x", padx=20, pady=(0, 15))

        self.info_frame = ctk.CTkFrame(self, fg_color="#232323")
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Scritta informativa interna in bianco lucido
        self.lbl_info = ctk.CTkLabel(self.info_frame, text=self.info_box_txt, text_color="white", font=ctk.CTkFont(size=13), justify="center")
        self.lbl_info.pack(expand=True, padx=20, pady=20)

        self.btn_execute = ctk.CTkButton(self, text=self.btn_exec_txt, command=self.execute_compression, font=ctk.CTkFont(size=14, weight="bold"), height=45, fg_color="#218838", hover_color="#28a745")
        self.btn_execute.pack(fill="x", padx=20, pady=(0, 20))

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
        if file_path:
            self.selected_file = file_path
            # Appende lo spazio vuoto protettivo sul testo in bianco lucido a caricamento avvenuto
            self.file_label.configure(text=os.path.basename(file_path) + " ", text_color="white")

    def execute_compression(self):
        if not self.selected_file:
            messagebox.showwarning("PDFlash", self.warning_select)
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("File PDF", "*.pdf")])
        if output_path:
            try:
                # Calcolo della dimensione iniziale in Megabyte
                orig_size = os.path.getsize(self.selected_file) / (1024 * 1024)

                reader = PdfReader(self.selected_file)
                writer = PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                # Attivazione dell'algoritmo di compressione dei flussi binari della pagina
                for page in writer.pages:
                    page.compress_content_streams()

                with open(output_path, "wb") as f:
                    writer.write(f)

                # Calcolo della nuova dimensione compressa
                comp_size = os.path.getsize(output_path) / (1024 * 1024)

                # Finestra di esito con i dettagli sul risparmio di peso in MB
                messagebox.showinfo("PDFlash", self.success_txt.format(orig=orig_size, comp=comp_size))
                
                self.selected_file = None
                self.file_label.configure(text=self.lbl_file_txt, text_color="gray")
            except Exception as e:
                messagebox.showerror("PDFlash", f"Error: {str(e)}")
