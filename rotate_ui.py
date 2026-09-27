import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter

class PDFRotatorUI(ctk.CTkFrame):
    def __init__(self, master, lang="EN", **kwargs):
        super().__init__(master, **kwargs)
        self.selected_file = None
        self.angle = ctk.IntVar(value=90)

        if lang == "IT":
            self.btn_select_txt = "📁  Seleziona il File PDF da Ruotare"
            self.lbl_file_txt = "Nessun file selezionato "
            self.lbl_angle_txt = "Scegli l'angolo di rotazione (orario):"
            self.btn_exec_txt = "🔄  RUOTA E SALVA PDF"
            self.warning_select = "Seleziona prima un file PDF."
            self.success_txt = "Documento ruotato e salvato con successo!"
        elif lang == "DE":
            self.btn_select_txt = "📁  PDF-Datei zum Drehen auswählen"
            self.lbl_file_txt = "Keine Datei ausgewählt "
            self.lbl_angle_txt = "Wählen Sie den Drehwinkel (im Uhrzeigersinn):"
            self.btn_exec_txt = "🔄  PDF DREHEN UND SPEICHERN"
            self.warning_select = "Bitte wählen Sie zuerst eine PDF-Datei aus."
            self.success_txt = "Dokument erfolgreich gedreht und gespeichert!"
        elif lang == "FR":
            self.btn_select_txt = "📁  Sélectionner le fichier PDF à pivoter"
            self.lbl_file_txt = "Aucun fichier sélectionné "
            self.lbl_angle_txt = "Choisissez l'angle de rotation (sens horaire) :"
            self.btn_exec_txt = "🔄  PIVOTER ET ENREGISTRER"
            self.warning_select = "Veuillez d'abord sélectionner un fichier PDF."
            self.success_txt = "Document pivoté et enregistré avec succès !"
        elif lang == "ES":
            self.btn_select_txt = "📁  Seleccionar archivo PDF para rotar"
            self.lbl_file_txt = "Ningún archivo seleccionado "
            self.lbl_angle_txt = "Elija el ángulo de rotación (sentido horario):"
            self.btn_exec_txt = "🔄  ROTAR Y GUARDAR PDF"
            self.warning_select = "Por favor, seleccione primero un archivo PDF."
            self.success_txt = "¡Documento rotado y guardado con éxito!"
        else:
            self.btn_select_txt = "📁  Select PDF File to Rotate"
            self.lbl_file_txt = "No file selected "
            self.lbl_angle_txt = "Choose rotation angle (clockwise):"
            self.btn_exec_txt = "🔄  ROTATE AND SAVE PDF"
            self.warning_select = "Please select a PDF file first."
            self.success_txt = "Document rotated and saved successfully!"

        self.btn_select = ctk.CTkButton(self, text=self.btn_select_txt, command=self.select_file, height=38)
        self.btn_select.pack(fill="x", padx=20, pady=(20, 10))

        self.file_label = ctk.CTkLabel(self, text=self.lbl_file_txt, text_color="gray", font=ctk.CTkFont(size=12, slant="italic"), justify="center")
        self.file_label.pack(fill="x", padx=20, pady=(0, 15))

        self.rotate_frame = ctk.CTkFrame(self, fg_color="#232323")
        self.rotate_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # FIX COLORE: text_color="white" forzato per la leggibilità del titolo
        self.lbl_angle = ctk.CTkLabel(self.rotate_frame, text=self.lbl_angle_txt, text_color="white", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_angle.pack(anchor="w", padx=20, pady=(15, 10))

        # FIX COLORE: text_color="white" per i radio button delle opzioni
        self.r90 = ctk.CTkRadioButton(self.rotate_frame, text="90°", text_color="white", variable=self.angle, value=90)
        self.r90.pack(anchor="w", padx=30, pady=5)

        self.r180 = ctk.CTkRadioButton(self.rotate_frame, text="180°", text_color="white", variable=self.angle, value=180)
        self.r180.pack(anchor="w", padx=30, pady=5)

        self.r270 = ctk.CTkRadioButton(self.rotate_frame, text="270°", text_color="white", variable=self.angle, value=270)
        self.r270.pack(anchor="w", padx=30, pady=5)

        self.btn_execute = ctk.CTkButton(self, text=self.btn_exec_txt, command=self.execute_rotation, font=ctk.CTkFont(size=14, weight="bold"), height=45, fg_color="#218838", hover_color="#28a745")
        self.btn_execute.pack(fill="x", padx=20, pady=(0, 20))

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
        if file_path:
            self.selected_file = file_path
            self.file_label.configure(text=os.path.basename(file_path) + " ", text_color="white")

    def execute_rotation(self):
        if not self.selected_file:
            messagebox.showwarning("PDFlash", self.warning_select)
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("File PDF", "*.pdf")])
        if output_path:
            try:
                reader = PdfReader(self.selected_file)
                writer = PdfWriter()
                deg = self.angle.get()

                for page in reader.pages:
                    page.rotate(deg)
                    writer.add_page(page)

                with open(output_path, "wb") as f:
                    writer.write(f)

                messagebox.showinfo("PDFlash", self.success_txt)
                self.selected_file = None
                self.file_label.configure(text=self.lbl_file_txt, text_color="gray")
            except Exception as e:
                messagebox.showerror("PDFlash", f"Error: {str(e)}")
