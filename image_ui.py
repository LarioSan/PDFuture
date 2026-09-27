# ==================== PARTE 1 DI 2 ====================
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import pymupdf as fitz 

class ImageToPDFUI(ctk.CTkFrame):
    def __init__(self, master, lang_dict=None, lang="EN", **kwargs):
        super().__init__(master, **kwargs)
        self.lang = lang
        self.image_list = []
        self.selected_pdf = None
        self.widgets_list = []
        
        # --- GESTIONE TRADUZIONI MULTILINGUA ---
        self.translations = {
            "EN": {
                "switch_static": "Switch mode",
                "mode_img_pdf": "Current: Photos ➔ PDF ",
                "mode_pdf_img": "Current: PDF ➔ Photos ",
                "add_images": "🖼️  Select Photos to Convert (JPG / PNG)",
                "select_pdf": "📁  Select the PDF File to Transform into Images",
                "empty_images": "No images loaded.\nClick the button above to add files to convert.",
                "empty_pdf": "No file selected ",
                "info_render": "⚙️ Rendering 300 DPI (High Quality JPG) ",
                "no_img_err": "No images loaded.",
                "no_pdf_err": "No file selected.",
                "select_folder": "Select Destination Folder"
            },
            "IT": {
                "switch_static": "Switch mode",
                "mode_img_pdf": "Corrente: Foto ➔ PDF ",
                "mode_pdf_img": "Corrente: PDF ➔ Foto ",
                "add_images": "🖼️  Seleziona Foto da Convertire (JPG / PNG)",
                "select_pdf": "📁  Seleziona il File PDF da Trasformare in Foto",
                "empty_images": "Nessuna immagine caricata.\nClicca sul pulsante in alto per aggiungere i file da convertire.",
                "empty_pdf": "Nessun file selezionato ",
                "info_render": "⚙️ Rendering 300 DPI (Alta Qualità JPG) ",
                "no_img_err": "Nessuna immagine caricata.",
                "no_pdf_err": "Nessun file selezionato.",
                "select_folder": "Seleziona Cartella di Destinazione"
            },
            "DE": {
                "switch_static": "Switch mode",
                "mode_img_pdf": "Aktuell: Bilder ➔ PDF ",
                "mode_pdf_img": "Aktuell: PDF ➔ Bilder ",
                "add_images": "🖼️  Bilder zum Konvertieren auswählen (JPG / PNG)",
                "select_pdf": "📁  Wählen Sie die PDF-Datei aus, um sie in Bilder umzuwandeln",
                "empty_images": "Keine Bilder geladen.\nKlicken Sie oben auf die Schaltfläche, um Dateien hinzuzufügen.",
                "empty_pdf": "Keine Datei ausgewählt ",
                "info_render": "⚙️ Rendering 300 DPI (Hohe Qualität JPG) ",
                "no_img_err": "Keine Bilder geladen.",
                "no_pdf_err": "Keine Datei ausgewählt.",
                "select_folder": "Zielordner auswählen"
            },
            "FR": {
                "switch_static": "Switch mode",
                "mode_img_pdf": "Actuel: Photos ➔ PDF ",
                "mode_pdf_img": "Actuel: PDF ➔ Photos ",
                "add_images": "🖼️  Sélectionner des photos à convertir (JPG / PNG)",
                "select_pdf": "📁  Sélectionnez le fichier PDF à transformer in images",
                "empty_images": "Aucune image chargée.\nCliquez au-dessus pour ajouter des fichiers.",
                "empty_pdf": "Aucun fichier sélectionné ",
                "info_render": "⚙️ Rendu 300 DPI (JPG Haute Qualité) ",
                "no_img_err": "Aucune image chargée.",
                "no_pdf_err": "Aucun fichier sélectionné.",
                "select_folder": "Sélectionner le dossier de destination"
            },
            "ES": {
                "switch_static": "Switch mode",
                "mode_img_pdf": "Actual: Fotos ➔ PDF ",
                "mode_pdf_img": "Actual: PDF ➔ Fotos ",
                "add_images": "🖼️  Seleccionar fotos para convertir (JPG / PNG)",
                "select_pdf": "📁  Seleccione el archivo PDF para transformar en imágenes",
                "empty_images": "No hay imágenes cargadas.\nHaga clic en el botón de arriba para agregar archivos.",
                "empty_pdf": "Ningún archivo seleccionado ",
                "info_render": "⚙️ Renderizado 300 DPI (Alta Calidad JPG) ",
                "no_img_err": "No hay imágenes cargadas.",
                "no_pdf_err": "Ningún archivo seleccionado.",
                "select_folder": "Seleccionar carpeta de destino"
            }
        }

        current_trans = self.translations.get(self.lang, self.translations["EN"])

        # --- CONTAINER SUPERIORE SWITCH CENTRATO ---
        self.top_switch_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_switch_frame.pack(fill="x", pady=(5, 10))

        self.switch_inner_container = ctk.CTkFrame(self.top_switch_frame, fg_color="transparent")
        self.switch_inner_container.pack(anchor="center")

        self.mode_switch = ctk.CTkSwitch(
            self.switch_inner_container, 
            text="", 
            command=self.toggle_mode,
            progress_color="#888888",  
            fg_color="#4a4a4a",        
            button_color="#dbdbdb",    
            button_hover_color="white",
            width=45
        )
        self.mode_switch.pack(side="left", padx=(0, 10))

        self.text_label_frame = ctk.CTkFrame(self.switch_inner_container, fg_color="transparent")
        self.text_label_frame.pack(side="left")

        self.lbl_switch_static = ctk.CTkLabel(self.text_label_frame, text=current_trans["switch_static"], font=ctk.CTkFont(size=13, weight="bold"), text_color="white", anchor="w")
        self.lbl_switch_static.pack(anchor="w")

        self.lbl_mode_dynamic = ctk.CTkLabel(self.text_label_frame, text=current_trans["mode_img_pdf"], font=ctk.CTkFont(size=11, slant="italic"), text_color="#b0b0b0", anchor="w")
        self.lbl_mode_dynamic.pack(anchor="w")

        # --- PULSANTE DI AZIONE ---
        self.btn_action = ctk.CTkButton(self, text=current_trans["add_images"], text_color="white", command=self.handle_action_click, height=38)
        self.btn_action.pack(fill="x", padx=15, pady=(5, 10))
# ==================== PARTE 2 DI 2 ====================
        # --- AREA CENTRALE DINAMICA ---
        self.listbox_frame = ctk.CTkScrollableFrame(self, fg_color="#232323", height=135)
        self.listbox_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        self.placeholder_label = ctk.CTkLabel(
            self.listbox_frame, 
            text=current_trans["empty_images"], 
            text_color="gray", 
            font=ctk.CTkFont(size=13)
        )
        self.placeholder_label.pack(expand=True, pady=30)

        # --- STRUMENTI DI CONTROLLO INTERMEDI ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.btn_clear = ctk.CTkButton(
            self.control_frame, 
            text="Svuota Lista / Clear", 
            command=self.clear_list, 
            width=100, 
            fg_color="#6e1a1a", 
            hover_color="#8a2323"
        )
        self.btn_clear.pack(side="right")

        # --- PULSANTE DI ESECUZIONE CORRETTO (AGGANCIATO A MASTER) ---
        self.btn_execute = ctk.CTkButton(
            master, 
            text="⚡ EXECUTE", 
            command=self.execute_process, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            height=45, 
            fg_color="#218838", 
            hover_color="#28a745"
        )
        self.btn_execute.pack(fill="x", side="bottom", padx=15, pady=(0, 15))

    def toggle_mode(self):
        """ Cambia l'interfaccia e resetta i dati in base alla posizione dello switch """
        current_trans = self.translations.get(self.lang, self.translations["EN"])
        
        if self.mode_switch.get() == 1:
            self.lbl_mode_dynamic.configure(text=current_trans["mode_pdf_img"], text_color="#b0b0b0")
            self.btn_action.configure(text=current_trans["select_pdf"])
            self.btn_clear.pack_forget()
            self.image_list.clear()
            self.selected_pdf = None
            self.update_visual_interface()
        else:
            self.lbl_mode_dynamic.configure(text=current_trans["mode_img_pdf"], text_color="#b0b0b0")
            self.btn_action.configure(text=current_trans["add_images"])
            self.btn_clear.pack(side="right")
            self.image_list.clear()
            self.selected_pdf = None
            self.update_visual_interface()

    def handle_action_click(self):
        """ Smista il clic del primo pulsante in base alla modalità attiva dello switch """
        if self.mode_switch.get() == 0:
            files = filedialog.askopenfilenames(filetypes=[("Immagini", "*.jpg *.jpeg *.png")])
            if files:
                self.image_list.extend(files)
                self.update_visual_interface()
        else:
            file_path = filedialog.askopenfilename(filetypes=[("File PDF", "*.pdf")])
            if file_path:
                self.selected_pdf = file_path
                self.update_visual_interface()

    def update_visual_interface(self):
        """ Svuota e aggiorna l'area centrale in base alla modalità e ai file caricati """
        current_trans = self.translations.get(self.lang, self.translations["EN"])
        
        for w in self.widgets_list:
            w.destroy()
        self.widgets_list.clear()
        
        if self.mode_switch.get() == 0:
            if not self.image_list:
                self.placeholder_label.configure(text=current_trans["empty_images"], text_color="gray", font=ctk.CTkFont(size=13))
                self.placeholder_label.pack(expand=True, pady=30)
                return
            self.placeholder_label.pack_forget()
            for img_path in self.image_list:
                lbl = ctk.CTkLabel(self.listbox_frame, text=f"📷 {os.path.basename(img_path)}", anchor="w")
                lbl.pack(fill="x", pady=2, padx=10)
                self.widgets_list.append(lbl)
        else:
            if not self.selected_pdf:
                self.placeholder_label.configure(text=current_trans["empty_pdf"], text_color="gray", font=ctk.CTkFont(size=12, slant="italic"))
                self.placeholder_label.pack(expand=True, pady=30)
                return
            self.placeholder_label.pack_forget()
            
            lbl_pdf = ctk.CTkLabel(self.listbox_frame, text=f"📄 {os.path.basename(self.selected_pdf)} ", font=ctk.CTkFont(size=13, weight="bold"), text_color="white")
            lbl_pdf.pack(fill="x", pady=(15, 5), padx=10)
            self.widgets_list.append(lbl_pdf)
            
            lbl_info = ctk.CTkLabel(self.listbox_frame, text=current_trans["info_render"], font=ctk.CTkFont(size=12, slant="italic"), text_color="gray")
            lbl_info.pack(fill="x", pady=5, padx=10)
            self.widgets_list.append(lbl_info)

    def clear_list(self):
        self.image_list.clear()
        self.selected_pdf = None
        self.update_visual_interface()

    def execute_process(self):
        """ Gestisce l'esecuzione finale smistando tra le due conversioni """
        current_trans = self.translations.get(self.lang, self.translations["EN"])
        
        if self.mode_switch.get() == 0:
            if not self.image_list:
                messagebox.showwarning("PDFlash", current_trans["no_img_err"])
                return
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("File PDF", "*.pdf")])
            if output_path:
                try:
                    converted_images = []
                    for img_path in self.image_list:
                        img = Image.open(img_path)
                        img_rgb = img.convert("RGB")
                        converted_images.append(img_rgb)
                    first_img = converted_images[0]
                    rest_images = converted_images[1:] if len(converted_images) > 1 else []
                    first_img.save(output_path, "PDF", resolution=300.0, save_all=True, append_images=rest_images)
                    messagebox.showinfo("PDFlash", "Success!")
                    self.clear_list()
                except Exception as e:
                    messagebox.showerror("PDFlash", str(e))
        else:
            if not self.selected_pdf:
                messagebox.showwarning("PDFlash", current_trans["no_pdf_err"])
                return
            output_dir = filedialog.askdirectory(title=current_trans["select_folder"])
            if output_dir:
                try:
                    doc = fitz.open(self.selected_pdf)
                    base_name = os.path.splitext(os.path.basename(self.selected_pdf))[0]
                    zoom = 4.16
                    mat = fitz.Matrix(zoom, zoom)
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap(matrix=mat)
                        output_path = os.path.join(output_dir, f"{base_name}_page_{page_num + 1}.jpg")
                        pix.save(output_path)
                    messagebox.showinfo("PDFlash", "Success!")
                    self.clear_list()
                except Exception as e:
                    messagebox.showerror("PDFlash", str(e))
