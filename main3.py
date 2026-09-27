import os
import threading
import urllib.request
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

# Importazione dei moduli della suite
from split_ui import PDFSplitterUI
from image_ui import ImageToPDFUI
from burocrazia_ui import BurocraziaHubUI

import sys
import os

def resource_path(relative_path):
    """ Ottiene il percorso assoluto della risorsa, funziona sia in sviluppo che in .exe """
    try:
        # PyInstaller crea una cartella temporanea e memorizza il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Versione corrente del software locale
CURRENT_VERSION = "1.0.0"
# URL del file su GitHub contenente l'ultima versione. Sostituisci con il tuo link reale.
VERSION_CHECK_URL = "https://raw.githubusercontent.com/LarioSan/PDFuture/main/version.txt"
# URL della tua pagina di donazione Ko-fi
KOFI_URL = "https://ko-fi.com/pdfuture"

# ------------------- DIZIONARIO TOTALE DI TRADUZIONE DI TUTTI I MODULI -------------------
LANGUAGES = {
    "EN": {
        "menu_merge": "Merge PDF",
        "menu_split": "Split PDF",
        "menu_compress": "Compress PDF",
        "menu_rotate": "Rotate Pages",
        "menu_search": "Search Text",
        "menu_redact": "Obscure Words",
        "menu_imgtools": "Image Tools",
        "menu_burocrazia": "📜 Hub Bureaucracy",
        "title_merge": "PDF Merger Tool",
        "descr_merge": "Add multiple PDF files to combine them into a single chronological document.",
        "placeholder_merge": "No files selected.\nClick 'Add Files' below to begin.",
        "btn_add": "+ Add Files", "btn_up": "▲ Up", "btn_down": "▼ Down", "btn_clear": "Clear",
        "btn_execute_merge": "⚡ MERGE AND SAVE PDF",
        "warning_min_files": "Please select at least 2 PDF files to merge.",
        "success_title": "Success", "success_merge": "PDF files merged successfully!",
        "error_title": "Error",
        "title_split": "PDF Splitter Tool",
        "descr_split": "Extract custom page intervals or save every page independently.",
        "title_compress": "PDF Smart Compressor",
        "descr_compress": "Reduce file size significantly for government or institutional portal uploads.",
        "title_rotate": "Page Rotator Tool",
        "descr_rotate": "Rotate individual or multiple pages of your PDF document offline.",
        "title_search": "PDF Text Finder",
        "descr_search": "Search for specific words or phrases and locate their exact page numbers.",
        "title_redact": "Privacy-First Redaction Tool",
        "descr_redact": "Permanently delete and mask sensitive names, codes, or IBANs across all pages.",
        "title_imgtools": "Converter Image Tools",
        "descr_imgtools": "Convert images to PDF at 300 DPI or rasterize PDF pages into high-res JPG files.",
        "title_burocrazia": "Smart Bureaucracy Hub",
        "descr_burocrazia": "Generate contracts, tax forms and international receipts compliant with regulations in just a few clicks. 🌐",
        "btn_upgrade": "⚡ NEW UPDATE",
        "tooltip_upgrade": "New update available!\nClick to discover the new features.", # EN
        "label_support": "Support this project ⚡"
    },
    "IT": {
        "menu_merge": "Unisci PDF",
        "menu_split": "Dividi PDF",
        "menu_compress": "Comprimi PDF",
        "menu_rotate": "Ruota Pagine",
        "menu_search": "Cerca nel Testo",
        "menu_redact": "Oscura Parole",
        "menu_imgtools": "Strumenti Foto",
        "menu_burocrazia": "📜 Hub Burocratico",
        "title_merge": "Strumento di Unione PDF",
        "descr_merge": "Aggiungi più file PDF per unirli in un unico documento cronologico.",
        "placeholder_merge": "Nessun file selezionato.\nClicca su 'Aggiungi File' in basso per iniziare.",
        "btn_add": "+ Aggiungi File", "btn_up": "▲ Su", "btn_down": "▼ Giù", "btn_clear": "Svuota",
        "btn_execute_merge": "⚡ UNISCI E SALVA PDF",
        "warning_min_files": "Seleziona almeno 2 file PDF da unire.",
        "success_title": "Successo", "success_merge": "File PDF unito con successo!",
        "error_title": "Errore",
        "title_split": "Strumento di Divisione PDF",
        "descr_split": "Estrai intervalli di pagine o separa ogni pagina del tuo PDF in file indipendenti.",
        "title_compress": "Compressore Intelligente PDF",
        "descr_compress": "Riduci drasticamente il peso del file per caricarlo sui portali dello Stato (INPS, Entrate).",
        "title_rotate": "Strumento di Rotazione Pagine",
        "descr_rotate": "Ruota singoli fogli capovolti o intere sezioni del tuo documento PDF offline.",
        "title_search": "Cerca nel Testo PDF",
        "descr_search": "Digita parole o frasi parziali per individuare istantaneamente in quali pagine si trovano.",
        "title_redact": "Oscura Parole Privacy-First",
        "descr_redact": "Cancella e copri definitivamente nomi, codici o IBAN ripetuti in tutto il documento.",
        "title_imgtools": "Convertitore e Strumenti Foto",
        "descr_imgtools": "Trasforma immagini in PDF a 300 DPI o estrai le pagine di un PDF sotto forma di foto JPG.",
        "title_burocrazia": "Hub Burocratico Tascabile",
        "descr_burocrazia": "Genera contratti, moduli fiscali e ricevute internazionali a norma in pochi clic. 🌐",
        "btn_upgrade": "⚡ NUOVO AGGIORNAMENTO",
        "tooltip_upgrade": "Nuovo aggiornamento disponibile!\nClicca per scoprire le nuove funzionalità.", # IT
        "label_support": "Supporta questo progetto ⚡"
    },
    "DE": {
        "menu_merge": "PDF zusammenführen",
        "menu_split": "PDF teilen",
        "menu_compress": "PDF komprimieren",
        "menu_rotate": "Seiten drehen",
        "menu_search": "Text suchen",
        "menu_redact": "Wörter schwärzen",
        "menu_imgtools": "Bildwerkzeuge",
        "menu_burocrazia": "📜 Bürokratiestudio",
        "title_merge": "PDF zusammenführen",
        "descr_merge": "Fügen Sie mehrere PDF-Dateien hinzu, um sie in einem Dokument zu kombinieren.",
        "placeholder_merge": "Keine Dateien ausgewählt.\nKlicken Sie unten auf 'Dateien hinzufügen'.",
        "btn_add": "+ Hinzufügen", "btn_up": "▲ Hoch", "btn_down": "▼ Runter", "btn_clear": "Leeren",
        "btn_execute_merge": "⚡ PDF ZUSAMMENFÜHREN",
        "warning_min_files": "Bitte wählen Sie mindestens 2 PDF-Dateien aus.",
        "success_title": "Erfolgreich", "success_merge": "PDF-Dateien erfolgreich zusammengeführt!",
        "error_title": "Fehler",
        "title_split": "PDF teilen",
        "descr_split": "Extrahieren Sie Seitenbereiche oder speichern Sie jede Seite separat.",
        "title_compress": "Intelligenter PDF-Kompressor",
        "descr_compress": "Dateigröße für Uploads auf Behördenportale drastisch reduzieren.",
        "title_rotate": "Seiten-Drehwerkzeug",
        "descr_rotate": "Einzelne oder mehrere Seiten Ihres PDF-Dokuments offline drehen.",
        "title_search": "Textfinder im PDF",
        "descr_search": "Suchen Sie nach bestimmten Wörtern und finden Sie deren genaue Seitenzahlen.",
        "title_redact": "Schwärzungstool (Datenschutz)",
        "descr_redact": "Sensible Namen, Codes oder IBANs auf allen Seiten endgültig löschen und maskieren.",
        "title_imgtools": "Bild-Konverter-Tools",
        "descr_imgtools": "Convertieren Sie Bilder in PDF (300 DPI) or rastern Sie PDF-Seiten in JPG-Dateien.",
        "title_burocrazia": "Bürokratie-Studio",
        "descr_burocrazia": "Erstellen Sie mit wenigen Klicks rechtskonforme Verträge, Steuerformulare und internationale Belege. 🌐",
        "btn_upgrade": "⚡ NEUES UPDATE",
        "tooltip_upgrade": "Neues Update verfügbar!\nKlicken , um die neuen Funktionen zu entdecken.", # DE
        "label_support": "Unterstütze dieses Projekt ⚡"
    },
    "FR": {
        "menu_merge": "Fusionner PDF",
        "menu_split": "Diviser PDF",
        "menu_compress": "Compresser PDF",
        "menu_rotate": "Pivoter Pages",
        "menu_search": "Chercher Texte",
        "menu_redact": "Masquer Mots",
        "menu_imgtools": "Outils d'Image",
        "menu_burocrazia": "📜 Hub Bureaucratique",
        "title_merge": "Outil de fusion PDF",
        "descr_merge": "Ajoutez plusieurs fichiers PDF pour les combiner en un seul document.",
        "placeholder_merge": "Aucun fichier sélectionné.\nCliquez sur 'Ajouter des fichiers' ci-dessous.",
        "btn_add": "+ Ajouter", "btn_up": "▲ Haut", "btn_down": "▼ Bas", "btn_clear": "Vider",
        "btn_execute_merge": "⚡ FUSIONNER ET ENREGISTRER",
        "warning_min_files": "Veuillez sélectionner au moins 2 fichiers PDF.",
        "success_title": "Succès", "success_merge": "Fichiers PDF fusionnés avec succès !",
        "error_title": "Erreur",
        "title_split": "Outil di division PDF",
        "descr_split": "Extrayez des intervalles de pages ou séparez chaque page indépendamment.",
        "title_compress": "Compresseur PDF Intelligent",
        "descr_compress": "Réduisez considérablement la taille du fichier pour les téléversements institutionnels.",
        "title_rotate": "Outil de rotation des pages",
        "descr_rotate": "Faites pivoter des pages individuelles ou multiples de votre document PDF hors ligne.",
        "title_search": "Recherche de texte PDF",
        "descr_search": "Recherchez des mots spécifiques et localisez leurs numéros de page exacts.",
        "title_redact": "Outil de masquage de données",
        "descr_redact": "Supprimez définitivement et masquez les noms ou IBAN sensibles sur toutes les pages.",
        "title_imgtools": "Outils de conversion d'images",
        "descr_imgtools": "Convertissez des images en PDF à 300 DPI ou transformez des pages PDF en fichiers JPG.",
        "title_burocrazia": "Hub Bureaucratique",
        "descr_burocrazia": "Générez des contrats, des formulaires fiscaux et des reçus internationaux conformes en quelques clics. 🌐",
        "btn_upgrade": "⚡ MISE À JOUR",
        "tooltip_upgrade": "Nouvelle mise à jour disponible !\nCliquez pour découvrir les nouvelles fonctionnalités.", # FR
        "label_support": "Soutenir ce projet ⚡"
    },
    "ES": {
        "menu_merge": "Unir PDF",
        "menu_split": "Dividir PDF",
        "menu_compress": "Comprimir PDF",
        "menu_rotate": "Rotar Páginas",
        "menu_search": "Buscar Texto",
        "menu_redact": "Ocultar Palabras",
        "menu_imgtools": "Herramientas Foto",
        "menu_burocrazia": "📜 Hub Burocrático",
        "title_merge": "Unir PDF",
        "descr_merge": "Agregue varios archivos PDF para combinarlos en un solo documento.",
        "placeholder_merge": "No hay archivos seleccionados.\nHaga clic en 'Agregar archivos' abajo.",
        "btn_add": "+ Agregar", "btn_up": "▲ Arriba", "btn_down": "▼ Abajo", "btn_clear": "Vaciar",
        "btn_execute_merge": "⚡ UNIR Y GUARDAR PDF",
        "warning_min_files": "Por favor, seleccione al menos 2 archivos PDF para unir.",
        "success_title": "Éxito", "success_merge": "¡Archivos PDF unidos con éxito!",
        "error_title": "Error",
        "title_split": "Herramienta de división PDF",
        "descr_split": "Extraiga intervalos di páginas personalizados o guarde cada página por separado.",
        "title_compress": "Compresor PDF Inteligente",
        "descr_compress": "Reduzca el tamaño del archivo para cargas en portales gubernamentales o institucionales.",
        "title_rotate": "Herramienta de rotación de páginas",
        "descr_rotate": "Rote páginas individuales o múltiples di su documento PDF fuera de línea.",
        "title_search": "Buscador de texto PDF",
        "descr_search": "Busque palabras específicas y locate sus números de página exactos.",
        "title_redact": "Herramienta de ocultación confidencial",
        "descr_redact": "Elimine permanentemente y oculte nombres, códigos o IBAN en todas las páginas.",
        "title_imgtools": "Herramientas de conversión di imágenes",
        "descr_imgtools": "Convierta imágenes en PDF a 300 DPI o transforme páginas PDF en archivos JPG nítidos.",
        "title_burocrazia": "Hub Burocrático",
        "descr_burocrazia": "Genere contratos, formularios fiscales y recibos internacionales conformes con las normas en pocos clics. 🌐",
        "btn_upgrade": "⚡ ACTUALIZAR",
        "tooltip_upgrade": "¡Nueva actualización disponible!\nHaga clic para descubrir las nuevas funciones.", # ES
        "label_support": "Apoya este proyecto ⚡"
    }
}

class HubPraticheLegali(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = "EN" 
        self.current_tab = "Unione" 
        self.title("PDFuture - The Future of PDF")
        
        # CORRETTO: Usa resource_path per trovare l'icona dentro il pacchetto .exe
        self.iconbitmap(resource_path("icona.ico"))

        
        # Dimensioni fisse della finestra attuale
        window_width = 890
        window_height = 600

        # Calcolo di base della risoluzione dello schermo
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Formula calibrata con offset manuale per compensare lo sfasamento a sinistra di Windows
        # Aggiungiamo pixel alla X (destra) e ne togliamo alla Y (in alto)
        center_x = int((screen_width / 2) - (window_width / 2)) + 60
        center_y = int((screen_height / 2) - (window_height / 2)) - 40

        # Imposta la geometria perfettamente bilanciata
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resizable(False, False)


        self.pdf_list = []
        self.btn_upgrade_element = None  # Riferimento per il pulsante di aggiornamento

        # ------------------- BARRA LATERALE (260px) -------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="⚡ PDFuture", font=ctk.CTkFont(size=20, weight="bold"))
        # SPOSTAMENTO DI UNA LETTERA: togliamo anchor="w" e usiamo un margine asimmetrico
        self.logo_label.pack(padx=(10, 30), pady=20)


        # Selettore Grafico Lingue
        self.lang_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.lang_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.lang_label = ctk.CTkLabel(self.lang_frame, text="🌐 Language:", font=ctk.CTkFont(size=12))
        self.lang_label.pack(side="left", padx=(5, 10))
        
        self.lang_menu = ctk.CTkOptionMenu(self.lang_frame, values=["EN", "IT", "DE", "FR", "ES"], width=80, height=25, command=self.change_language)
        self.lang_menu.set("EN")
        self.lang_menu.pack(side="left")

        # Contenitore pulsanti menu
        self.menu_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.menu_container.pack(fill="x", padx=15, pady=5)

        self.menu_buttons = {}
        self.setup_sidebar_menu()
                # AREA SUPPORT (POSIZIONE DELLA VITTORIA CON FONT PIÙ GRANDE E IN GRASSETTO)
        self.sponsor_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.sponsor_frame.pack(side="bottom", fill="x", padx=15, pady=(0, 85))

        self.support_label = ctk.CTkLabel(
            self.sponsor_frame, 
            text=LANGUAGES[self.current_lang]["label_support"], 
            # Ripristinato font dimensione 13, in grassetto (bold) e corsivo (italic) per massima visibilità
            font=ctk.CTkFont(size=13, weight="bold", slant="italic"),
            text_color="#a0a0a0", 
            wraplength=220,
            cursor="hand2",
            justify="left",  
            anchor="w"       
        )
        self.support_label.pack(fill="x", anchor="w", padx=(15, 0)) 
        self.support_label.bind("<Button-1>", lambda e: webbrowser.open(KOFI_URL))
        self.support_label.bind("<Enter>", lambda e: self.support_label.configure(text_color="#FFEFCB"))
        self.support_label.bind("<Leave>", lambda e: self.support_label.configure(text_color="#a0a0a0"))


        # --- ANCORAGGIO STABILE IN ALTO PER IL PULSANTE HUB ---
        self.top_bar_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_bar_frame.pack(fill="x", side="top", pady=(0, 5))

        self.btn_hub_burocrazia = ctk.CTkButton(
            self.top_bar_frame, 
            text=LANGUAGES[self.current_lang]["menu_burocrazia"], 
            width=140, 
            height=32, 
            font=ctk.CTkFont(size=12, weight="bold"), 
            fg_color="#A9874A", 
            text_color="#FFEFCB", 
            hover_color="#91733E",
            corner_radius=6,
            command=lambda: self.switch_tab("Burocrazia")
        )
        self.btn_hub_burocrazia.pack(side="right")
        self.titles_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.titles_frame.pack(fill="x", side="top", pady=(0, 15))

        self.title_main = ctk.CTkLabel(self.titles_frame, text="", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_main.pack(anchor="w")

        self.descr_main = ctk.CTkLabel(self.titles_frame, text="", text_color="gray", font=ctk.CTkFont(size=13))
        self.descr_main.pack(anchor="w", pady=(2, 0))

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b")
        self.content_frame.pack(fill="both", expand=True)

        self.refresh_ui_text()
        self.setup_merge_ui()
        
        # Chiamata in background sicura e ultra-veloce su GitHub
        threading.Thread(target=self.check_for_updates, daemon=True).start()
   
    def check_for_updates(self):
        def async_worker():
            import time
            # Aspetta 2 secondi in background dall'avvio per creare l'effetto comparsa tardiva
            time.sleep(2)
            try:
                req = urllib.request.Request(VERSION_CHECK_URL, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=4) as response:
                    remote_version = response.read().decode('utf-8').strip()
                    # Il tasto compare ONLINE nel mondo reale SOLO se la versione su GitHub è diversa da quella locale
                    if remote_version and remote_version != CURRENT_VERSION:
                        self.after(0, self.show_upgrade_button)
            except Exception:
                pass  # Silenzioso se l'utente è offline o GitHub ha problemi momentanei

        # Avvia il thread separato in background per la massima velocità all'avvio
        threading.Thread(target=async_worker, daemon=True).start()

    def show_upgrade_button(self):
        if self.btn_upgrade_element is None:
            # Creazione del micro badge adattivo e stabile con i parametri esatti approvati
            self.btn_upgrade_element = ctk.CTkButton(
                self,
                text=LANGUAGES[self.current_lang]["btn_upgrade"],
                width=0,            
                height=18,          
                font=ctk.CTkFont(size=9, weight="bold"), 
                fg_color="#A9874A",
                text_color="#FFEFCB",
                hover_color="#91733E",
                corner_radius=9,
                # Apre stabilmente il link di rilascio di GitHub al clic del mouse
                command=lambda: webbrowser.open("https://github.com")
            )
            # La coordinata perfetta calibrata in asse con il tasto di esecuzione verde
            self.btn_upgrade_element.place(relx=0.5, rely=1.0, x=145, y=-6, anchor="s")
            
            self.upgrade_tooltip_window = None
            
            # Collega gli eventi del mouse per il tooltip auto-pulente corazzato
            self.btn_upgrade_element.bind("<Enter>", lambda e: self.show_upgrade_tooltip())
            self.btn_upgrade_element.bind("<Leave>", lambda e: self.hide_upgrade_tooltip())

    def show_upgrade_tooltip(self):
        # Chiude preventivamente qualsiasi residuo precedente
        self.hide_upgrade_tooltip()
            
        if not self.btn_upgrade_element:
            return
            
        # Calcola la posizione esatta sopra il tastino centrato
        x = self.btn_upgrade_element.winfo_rootx() - 40
        y = self.btn_upgrade_element.winfo_rooty() - 45
        
        self.upgrade_tooltip_window = ctk.CTkToplevel(self)
        self.upgrade_tooltip_window.wm_overrideredirect(True)
        self.upgrade_tooltip_window.wm_geometry(f"+{x}+{y}")
        self.upgrade_tooltip_window.attributes("-topmost", True)
        
        label = ctk.CTkLabel(
            self.upgrade_tooltip_window,
            text=LANGUAGES[self.current_lang]["tooltip_upgrade"],
            fg_color="#1a1a1a",
            text_color="#FFEFCB",
            font=ctk.CTkFont(size=10, slant="italic"),
            padx=8,
            pady=4,
            corner_radius=4
        )
        label.pack()
        
        # Mantiene attivo il controllo di prossimità asincrono infallibile ad alta frequenza
        self.auto_clean_tooltip_loop()

    def auto_clean_tooltip_loop(self):
        if hasattr(self, 'upgrade_tooltip_window') and self.upgrade_tooltip_window:
            if self.btn_upgrade_element:
                mouse_x = self.winfo_pointerx()
                mouse_y = self.winfo_pointery()
                
                btn_x1 = self.btn_upgrade_element.winfo_rootx()
                btn_y1 = self.btn_upgrade_element.winfo_rooty()
                btn_x2 = btn_x1 + self.btn_upgrade_element.winfo_width()
                btn_y2 = btn_y1 + self.btn_upgrade_element.winfo_height()
                
                if not (btn_x1 <= mouse_x <= btn_x2 and btn_y1 <= mouse_y <= btn_y2):
                    self.hide_upgrade_tooltip()
                    return
            
            self.after(200, self.auto_clean_tooltip_loop)

    def hide_upgrade_tooltip(self):
        if hasattr(self, 'upgrade_tooltip_window') and self.upgrade_tooltip_window:
            try:
                self.upgrade_tooltip_window.destroy()
            except Exception:
                pass
            self.upgrade_tooltip_window = None



    def setup_sidebar_menu(self):
        for widget in self.menu_container.winfo_children():
            widget.destroy()
            
        def crea_bottone(testo_key, tab_id, fg_bg="transparent", txt_col="white"):
            testo_completo = LANGUAGES[self.current_lang][testo_key]
            btn = ctk.CTkButton(self.menu_container, text=testo_completo, anchor="w", font=ctk.CTkFont(size=13, weight="bold"), height=35, fg_color=fg_bg, text_color=txt_col, corner_radius=6, command=lambda: self.switch_tab(tab_id))
            btn.pack(fill="x", pady=3, padx=15)
            self.menu_buttons[tab_id] = btn

        crea_bottone("menu_merge", "Unione", fg_bg="#1f538d" if self.current_tab == "Unione" else "transparent")
        crea_bottone("menu_split", "Divisione", fg_bg="#1f538d" if self.current_tab == "Divisione" else "transparent")
        crea_bottone("menu_compress", "Compressione", fg_bg="#1f538d" if self.current_tab == "Compressione" else "transparent")
        crea_bottone("menu_rotate", "Rotazione", fg_bg="#1f538d" if self.current_tab == "Rotazione" else "transparent")
        crea_bottone("menu_search", "Ricerca", fg_bg="#1f538d" if self.current_tab == "Ricerca" else "transparent")
        crea_bottone("menu_redact", "Oscuramento", fg_bg="#1f538d" if self.current_tab == "Oscuramento" else "transparent")
        crea_bottone("menu_imgtools", "FotoTools", fg_bg="#1f538d" if self.current_tab == "FotoTools" else "transparent")

    def change_language(self, new_lang):
        self.current_lang = new_lang
        self.setup_sidebar_menu()
        self.refresh_ui_text()
        self.switch_tab(self.current_tab)
        # Aggiorna istantaneamente la lingua della scritta di supporto
        self.support_label.configure(text=LANGUAGES[self.current_lang]["label_support"])
        if self.btn_upgrade_element:
            self.btn_upgrade_element.configure(text=LANGUAGES[self.current_lang]["btn_upgrade"])

    def refresh_ui_text(self):
        self.title("PDFuture - The Future of PDF")
        self.btn_hub_burocrazia.configure(text=LANGUAGES[self.current_lang]["menu_burocrazia"])
        
        if self.current_tab == "Unione":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_merge"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_merge"])
        elif self.current_tab == "Divisione":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_split"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_split"])
        elif self.current_tab == "Compressione":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_compress"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_compress"])
        elif self.current_tab == "Rotazione":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_rotate"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_rotate"])
        elif self.current_tab == "Ricerca":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_search"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_search"])
        elif self.current_tab == "Oscuramento":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_redact"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_redact"])
        elif self.current_tab == "FotoTools":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_imgtools"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_imgtools"])
        elif self.current_tab == "Burocrazia":
            self.title_main.configure(text=LANGUAGES[self.current_lang]["title_burocrazia"])
            self.descr_main.configure(text=LANGUAGES[self.current_lang]["descr_burocrazia"])
    def setup_merge_ui(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.listbox_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="#232323")
        self.listbox_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.placeholder_label = ctk.CTkLabel(self.listbox_frame, text=LANGUAGES[self.current_lang]["placeholder_merge"], text_color="gray", font=ctk.CTkFont(size=13))
        self.placeholder_label.pack(expand=True, pady=60)

        self.control_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.control_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.btn_add = ctk.CTkButton(self.control_frame, text=LANGUAGES[self.current_lang]["btn_add"], command=self.add_files, width=120)
        self.btn_add.pack(side="left", padx=(0, 10))

        self.btn_up = ctk.CTkButton(self.control_frame, text=LANGUAGES[self.current_lang]["btn_up"], command=self.move_up, width=70, fg_color="#333333", text_color="white")
        self.btn_up.pack(side="left", padx=5)

        self.btn_down = ctk.CTkButton(self.control_frame, text=LANGUAGES[self.current_lang]["btn_down"], command=self.move_down, width=70, fg_color="#333333", text_color="white")
        self.btn_down.pack(side="left", padx=5)

        self.btn_clear = ctk.CTkButton(self.control_frame, text=LANGUAGES[self.current_lang]["btn_clear"], command=self.clear_list, width=80, fg_color="#6e1a1a", hover_color="#8a2323")
        self.btn_clear.pack(side="right")

        self.btn_execute_merge = ctk.CTkButton(self.content_frame, text=LANGUAGES[self.current_lang]["btn_execute_merge"], command=self.merge_pdfs, font=ctk.CTkFont(size=14, weight="bold"), height=45, fg_color="#218838", hover_color="#28a745")
        self.btn_execute_merge.pack(fill="x", side="bottom", padx=15, pady=(0, 15))

        self.selected_index = None
        self.buttons_widgets = []
        self.update_listbox()

    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        
        for t_id, btn in self.menu_buttons.items():
            btn.configure(fg_color="transparent", text_color="white")

        if tab_name in self.menu_buttons:
            self.menu_buttons[tab_name].configure(fg_color="#1f538d", text_color="white")

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.refresh_ui_text()

        self.title_main.pack(anchor="w")
        self.descr_main.configure(wraplength=550, justify="left")
        self.descr_main.pack(anchor="w", pady=(2, 0))

        if tab_name == "Unione":
            self.setup_merge_ui()
        elif tab_name == "Divisione":
            self.splitter_frame = PDFSplitterUI(self.content_frame, lang_dict=LANGUAGES, lang=self.current_lang, fg_color="transparent")
            self.splitter_frame.pack(fill="both", expand=True)
        elif tab_name == "Compressione":
            try:
                from compress_ui import PDFCompressorUI
                self.compress_frame = PDFCompressorUI(self.content_frame, lang=self.current_lang, fg_color="transparent")
                self.compress_frame.pack(fill="both", expand=True)
            except Exception: pass
        elif tab_name == "Rotazione":
            try:
                from rotate_ui import PDFRotatorUI
                self.rotate_frame = PDFRotatorUI(self.content_frame, lang=self.current_lang, fg_color="transparent")
                self.rotate_frame.pack(fill="both", expand=True)
            except Exception: pass
        elif tab_name == "Ricerca":
            try:
                from search_ui import PDFSearchUI
                self.search_frame = PDFSearchUI(self.content_frame, lang=self.current_lang, fg_color="transparent")
                self.search_frame.pack(fill="both", expand=True)
            except Exception: pass
        elif tab_name == "Oscuramento":
            try:
                from redact_ui import PDFRedactUI
                self.redact_frame = PDFRedactUI(self.content_frame, lang=self.current_lang, fg_color="transparent")
                self.redact_frame.pack(fill="both", expand=True)
            except Exception: pass
        elif tab_name == "FotoTools":
            self.image_frame = ImageToPDFUI(self.content_frame, lang_dict=LANGUAGES, lang=self.current_lang, fg_color="transparent")
            self.image_frame.pack(fill="both", expand=True)
        elif tab_name == "Burocrazia":
            self.burocrazia_frame = BurocraziaHubUI(self.content_frame, lang=self.current_lang, fg_color="transparent")
            self.burocrazia_frame.pack(fill="both", expand=True)

    def update_listbox(self):
        for widget in self.buttons_widgets:
            widget.destroy()
        self.buttons_widgets.clear()
        if not self.pdf_list:
            self.placeholder_label.pack(expand=True, pady=60)
            return
        self.placeholder_label.pack_forget()
        for idx, file_path in enumerate(self.pdf_list):
            file_name = os.path.basename(file_path)
            bg_color = "#2b2b2b" if idx != self.selected_index else "#1f538d"
            btn = ctk.CTkButton(self.listbox_frame, text=f"{idx + 1}. {file_name}", anchor="w", fg_color=bg_color, hover_color="#3e3e3e", command=lambda i=idx: self.select_item(i))
            btn.pack(fill="x", pady=2, padx=5)
            self.buttons_widgets.append(btn)

    def select_item(self, index):
        self.selected_index = index
        self.update_listbox()

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("File PDF", "*.pdf")])
        if files:
            for f in files:
                if f not in self.pdf_list:
                    self.pdf_list.append(f)
            self.update_listbox()

    def clear_list(self):
        self.pdf_list.clear()
        self.selected_index = None
        self.update_listbox()

    def move_up(self):
        if self.selected_index is not None and self.selected_index > 0:
            idx = self.selected_index
            self.pdf_list[idx], self.pdf_list[idx-1] = self.pdf_list[idx-1], self.pdf_list[idx]
            self.selected_index -= 1
            self.update_listbox()

    def move_down(self):
        if self.selected_index is not None and self.selected_index < len(self.pdf_list) - 1:
            idx = self.selected_index
            self.pdf_list[idx], self.pdf_list[idx+1] = self.pdf_list[idx+1], self.pdf_list[idx]
            self.selected_index += 1
            self.update_listbox()

    def merge_pdfs(self):
        if len(self.pdf_list) < 2:
            messagebox.showwarning(LANGUAGES[self.current_lang]["error_title"], LANGUAGES[self.current_lang]["warning_min_files"])
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("File PDF", "*.pdf")])
        if output_path:
            try:
                merger = PdfWriter()
                for pdf in self.pdf_list:
                    merger.append(pdf)
                merger.write(output_path)
                merger.close()
                messagebox.showinfo(LANGUAGES[self.current_lang]["success_title"], LANGUAGES[self.current_lang]["success_merge"])
                self.clear_list()
            except Exception as e:
                messagebox.showerror(LANGUAGES[self.current_lang]["error_title"], f"Error:\n{str(e)}")

if __name__ == "__main__":
    app = HubPraticheLegali()
    app.mainloop()
