import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

class BurocraziaHubUI(ctk.CTkFrame):
    def __init__(self, master, lang="EN", **kwargs):
        super().__init__(master, **kwargs)
        self.lang = lang

        # Palette Colori Ufficiali e Approvati
        self.col_oro = "#A9874A"     
        self.col_crema = "#FFEFCB"   
        self.col_card_bg = "#333333" 
        self.col_canvas_bg = "#232323"

        # Stato della navigazione interna
        self.current_view = "canvas"  

        # ------------------- DIZIONARIO TRADUZIONI INTEGRALE DI TUTTI I MODULI INTERNI -------------------
        self.translations = {
            "EN": {
                "hub_title": " Smart Bureaucracy Hub",
                "btn_back": "◀ Back to Dashboard",
                "btn_generate": "⚡ GENERATE COMPLIANT PDF DOCUMENT",
                "pop_success": "Document generated successfully!",
                "err_fields": "Please fill in all required fields with valid data.",
                "switch_calc": "Calculation Mode",
                "mode_net": "Current: Input Net ➔ Calc Gross ", 
                "mode_gross": "Current: Input Gross ➔ Calc Net ",
                "t1_title": "Occasional Work Receipt", "t1_sub": "ONLY FOR ITALIANS",
                "lbl_worker_t1": "Your Personal Data (Name, Surname, Fiscal Code):",
                "lbl_client_t1": "Client / Company Data (VAT / Tax ID):",
                "lbl_amount_t1": "Amount (€):",
                "lbl_details_t1": "Note / Additional Specifications:",
                "t2_title": "W-8 BEN Assistant", "t2_sub": "US IRS Foreign Status Statement",
                "lbl_worker_t2": "1. Full Name of Beneficial Owner (Individual):",
                "lbl_client_t2": "2. Permanent Residence Address (Street, City, State, ZIP, Country):",
                "lbl_amount_t2": "3. Foreign Tax Identifying Number (e.g., Fiscal Code / Tax ID):",
                "lbl_details_t2": "4. Country of Citizenship / Residence Treaty:",
                "t3_title": "Mutual NDA Contract", "t3_sub": "International Non-Disclosure",
                "lbl_worker_t3": "First Party - Disclosing Entity (Your Name/Company):",
                "lbl_client_t3": "Second Party - Receiving Entity (Client/Counterparty Name):",
                "lbl_amount_t3": "Confidentiality Term / Duration (e.g., 3 years, 5 years):",
                "lbl_details_t3": "Project Scope / Purpose of Disclosure (e.g., Software Source Code):",
                "t4_title": "Cease & Desist Order", "t4_sub": "Copyright Infringement Notice",
                "lbl_worker_t4": "Copyright Owner Name (Your Full Name / Company):",
                "lbl_client_t4": "Infringer Identity (Name of Individual, Website, or Platform):",
                "lbl_amount_t4": "Compliance Deadline / Response Time (e.g., 10 days, 14 days):",
                "lbl_details_t4": "Description of Infringement (e.g., Unauthorized copying of Github Repository source code):"
            },
            "IT": {
                "hub_title": " Hub Burocratico Tascabile",
                "btn_back": "◀ Torna alla Dashboard",
                "btn_generate": "⚡ GENERA DOCUMENTO PDF A NORMA",
                "pop_success": "Documento creato con successo!",
                "err_fields": "Per favore, compila tutti i campi richiesti con dati validi.",
                "switch_calc": "Modalità Calcolo",
                "mode_net": "Corrente: Inserisci Netto ➔ Calcola Lordo ", 
                "mode_gross": "Corrente: Inserisci Lordo ➔ Calcola Netto ",
                "t1_title": "Ricevuta Occasionale", "t1_sub": "SOLO PER ITALIANI",
                "lbl_worker_t1": "Tuoi Dati Anagrafici (Nome, Cognome, CF):",
                "lbl_client_t1": "Dati Committente / Azienda (P.IVA/CF):",
                "lbl_amount_t1": "Cifra / Importo Operazione (€):",
                "lbl_details_t1": "Causale o Note Opzionali:",
                "t2_title": "Assistente W-8 BEN", "t2_sub": "Dichiarazione Fiscale Extra-USA",
                "lbl_worker_t2": "1. Nome Completo del Beneficiario (Individuo):",
                "lbl_client_t2": "2. Indirizzo di Residenza Permanente (Via, Città, CAP, Stato):",
                "lbl_amount_t2": "3. Codice di Identificazione Fiscale Estero (es. Codice Fiscale):",
                "lbl_details_t2": "4. Paese di Cittadinanza / Trattato di Residenza:",
                "t3_title": "Contratto NDA Mutuo", "t3_sub": "Accordo Riservatezza Internazionale",
                "lbl_worker_t3": "Prima Parte - Divulgante (Tuo Nome / Nome Azienda):",
                "lbl_client_t3": "Seconda Parte - Ricevente (Nome Cliente / Controparte):",
                "lbl_amount_t3": "Termine di Riservatezza / Durata del Vincolo (es. 3 anni, 5 anni):",
                "lbl_details_t3": "Ambito del Progetto / Oggetto della Segretezza (es. Codice Sorgente Software):",
                "t4_title": "Diffida Cease & Desist", "t4_sub": "Notifica Violazione Copyright",
                "lbl_worker_t4": "Nome del Titolare del Copyright (Tuo Nome / Azienda):",
                "lbl_client_t4": "Identità del Trasgressore (Nome di Individuo, Sito Web o Piattaforma):",
                "lbl_amount_t4": "Termine di Conformità / Tempo di Risposta (es. 10 giorni, 14 giorni):",
                "lbl_details_t4": "Descrizione della Violazione (es. Copia non autorizzata del codice sorgente della Repository GitHub):"
            },
            "DE": {
                "hub_title": " 📜 Bürokratiestudio",
                "btn_back": "◀ Zurück zum Dashboard",
                "btn_generate": "⚡ RECHTSKONFORMES PDF ERSTELLEN",
                "pop_success": "Dokument erfolgreich erstellt!",
                "err_fields": "Bitte füllen Sie alle erforderlichen Felder mit gültigen Daten aus.",
                "switch_calc": "Berechnungsmodus",
                "mode_net": "Aktuell: Netto eingeben ➔ Brutto berechnen ", 
                "mode_gross": "Aktuell: Brutto eingeben ➔ Netto berechnen ",
                "t1_title": "Gelegentliche Quittung", "t1_sub": "NUR FÜR ITALIENER",
                "lbl_worker_t1": "Ihre persönlichen Daten (Name, Steuernummer):",
                "lbl_client_t1": "Daten des Auftraggebers / Unternehmens (USt-IdNr):",
                "lbl_amount_t1": "Betrag (€):",
                "lbl_details_t1": "Grund oder optionale Hinweise:",
                "t2_title": "W-8 BEN Assistent", "t2_sub": "US IRS Erklärung für ausländischen Status",
                "lbl_worker_t2": "1. Vollständiger Name des wirtschaftlichen Eigentümers:",
                "lbl_client_t2": "2. Ständiger Wohnsitz (Straße, Stadt, PLZ, Land):",
                "lbl_amount_t2": "3. Ausländische Steueridentifikationsnummer (z. B. Steuernummer):",
                "lbl_details_t2": "4. Staatsangehörigkeit / Aufenthaltsabkommen:",
                "t3_title": "NDA-Vertrag (Gegenseitig)", "t3_sub": "Internationale Vertraulichkeit",
                "lbl_worker_t3": "Erste Partei - Offenlegende Stelle (Ihr Name/Unternehmen):",
                "lbl_client_t3": "Zweite Partei - Empfangende Stelle (Name des Kunden):",
                "lbl_amount_t3": "Vertraulichkeitsfrist / Dauer der Bindung (z. B. 3 Jahre):",
                "lbl_details_t3": "Projektumfang / Gegenstand della Geheimhaltung (z. B. Quellcode):",
                "t4_title": "Cease & Desist Anordnung", "t4_sub": "Abmahnung wegen Urheberrechtsverletzung",
                "lbl_worker_t4": "Name des Urheberrechtsinhabers (Ihr Name/Unternehmen):",
                "lbl_client_t4": "Identität des Verletzers (Name der Person, Website oder Plattform):",
                "lbl_amount_t4": "Frist für Compliance / Antwortzeit (z. B. 10 Tage):",
                "lbl_details_t4": "Beschreibung della Verletzung (z. B. Unbefugtes Kopieren von GitHub-Quellcode):"
            },
            "FR": {
                "hub_title": " 📜 Hub Bureaucratique",
                "btn_back": "◀ Retour au Tableau de Bord",
                "btn_generate": "⚡ GÉNÉRER LE DOCUMENT PDF CONFORME",
                "pop_success": "Document généré avec succès !",
                "err_fields": "Veuillez remplir tous les champs requis avec des données valides.",
                "switch_calc": "Mode de Calcul",
                "mode_net": "Actuel: Saisir Net ➔ Calculer Brut ", 
                "mode_gross": "Actuel: Saisir Brut ➔ Calculer Net ",
                "t1_title": "Reçu Occasionnel", "t1_sub": "UNIQUEMENT POUR LES ITALIENS",
                "lbl_worker_t1": "Vos données personnelles (Nom, Code Fiscal):",
                "lbl_client_t1": "Données du Client / Entreprise (N° TVA):",
                "lbl_amount_t1": "Montant (€):",
                "lbl_details_t1": "Motif ou notes optionnelles:",
                "t2_title": "Assistant W-8 BEN", "t2_sub": "Déclaration de statut étranger US IRS",
                "lbl_worker_t2": "1. Nom complet du bénéficiaire effectif (Individu):",
                "lbl_client_t2": "2. Adresse de résidence permanente (Rue, Ville, Code Postal, Pays):",
                "lbl_amount_t2": "3. Numéro d'identification fiscale étranger (ex. Code Fiscal):",
                "lbl_details_t2": "4. Pays de citoyenneté / Traité de résidence:",
                "t3_title": "Accord NDA Mutuel", "t3_sub": "Confidentialité Internationale",
                "lbl_worker_t3": "Première Partie - Entité Divulgatrice (Votre Nom/Entreprise):",
                "lbl_client_t3": "Seconde Partie - Entité Réceptrice (Nom du Client):",
                "lbl_amount_t3": "Durée de confidentialité / Durée de l'obligation (ex. 3 ans):",
                "lbl_details_t3": "Portée du projet / Objet du secret (ex. Code source du logiciel):",
                "t4_title": "Ordonnance Cease & Desist", "t4_sub": "Notification de violation du droit d'auteur",
                "lbl_worker_t4": "Nom du titulaire du droit d'auteur (Votre Nom/Entreprise):",
                "lbl_client_t4": "Identité du contrevenant (Nom de l'individu, site web ou plateforme):",
                "lbl_amount_t4": "Délai de conformité / Temps de réponse (ex. 10 jours):",
                "lbl_details_t4": "Description de la violation (ex. Copie non autorisée du code source du dépôt GitHub):"
            },
            "ES": {
                "hub_title": " 📜 Hub Burocrático",
                "btn_back": "◀ Volver al Panel de Control",
                "btn_generate": "⚡ GENERAR DOCUMENTO PDF CONFORRE",
                "pop_success": "¡Documento generado con éxito!",
                "err_fields": "Por favor, complete todos los campos requeridos con datos válidos.",
                "switch_calc": "Modo di Cálculo",
                "mode_net": "Actual: Introducir Neto ➔ Calcular Bruto ", 
                "mode_gross": "Actual: Introducir Brut ➔ Calcular Neto ",
                "t1_title": "Recibo Occasional", "t1_sub": "SOLO PARA ITALIANOS",
                "lbl_worker_t1": "Sus datos personales (Nombre, Apellido, Código Fiscal):",
                "lbl_client_t1": "Datos del Cliente / Empresa (CIF / Identificación Fiscal):",
                "lbl_amount_t1": "Cantidad (€):",
                "lbl_details_t1": "Concepto o notas opcionales:",
                "t2_title": "Asistente W-8 BEN", "t2_sub": "Declaración de estatus extranjero de la IRS de EE. UU.",
                "lbl_worker_t2": "1. Nombre completo del propietario beneficiario (Individuo):",
                "lbl_client_t2": "2. Dirección de residencia permanente (Calle, Ciudad, Código Postal, País):",
                "lbl_amount_t2": "3. Número de identificación fiscal extranjero (ej. Código Fiscal):",
                "lbl_details_t2": "4. País de ciudadanía / Tratado de residencia:",
                "t3_title": "Contratto NDA Mutuo", "t3_sub": "Confidencialidad Internacional",
                "lbl_worker_t3": "Primera Parte - Entidad Divulgadora (Su Nombre/Empresa):",
                "lbl_client_t3": "Segunda Parte - Entidad Receptora (Nombre del Cliente):",
                "lbl_amount_t3": "Término de confidencialidad / Duración de la obligación (ej. 3 anni):",
                "lbl_details_t3": "Alcance del proyecto / Objeto del secreto (ej. Código fuente del software):",
                "t4_title": "Orden Cease & Desist", "t4_sub": "Notificación de infracción de derechos de autor",
                "lbl_worker_t4": "Nombre del titular de los derechos de autor (Su Nombre/Empresa):",
                "lbl_client_t4": "Identidad del infractor (Nombre de la persona, sitio web o plataforma):",
                "lbl_amount_t4": "Plazo de cumplimiento / Tiempo de respuesta (ej. 10 días):",
                "lbl_details_t4": "Descripción de la infracción (ej. Código fuente del repositorio de GitHub):"
            }
        }
        self.show_canvas_dashboard()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def configure(self, **kwargs):
        if "lang" in kwargs:
            self.lang = kwargs.pop("lang")
            if self.current_view == "canvas":
                self.show_canvas_dashboard()
            else:
                self.open_tool_form(self.current_view)
        super().configure(**kwargs)
    def show_canvas_dashboard(self):
        self.current_view = "canvas"
        self.clear_frame()
        
        t = self.translations.get(self.lang, self.translations["EN"])

        self.lbl_title = ctk.CTkLabel(self, text=t["hub_title"], font=ctk.CTkFont(size=18, weight="bold"), text_color=self.col_crema, anchor="w")
        self.lbl_title.pack(fill="x", padx=25, pady=(15, 10))

        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        for i in range(4):
            self.grid_container.grid_columnconfigure(i, weight=1, uniform="equal")
        self.grid_container.grid_rowconfigure(0, weight=1)
        
        def crea_foglio_canvas(colonna, titolo, sottotitolo, target_view):
            # Aggiunta un'altezza minima fissa (min_height) alla card per contenere testi lunghi
            card = ctk.CTkFrame(self.grid_container, fg_color=self.col_card_bg, corner_radius=8, cursor="hand2")
            card.grid(row=0, column=colonna, padx=8, pady=10, sticky="nsew")
            
            card.bind("<Enter>", lambda e: card.configure(fg_color="#3d3d3d", border_color=self.col_oro, border_width=1))
            card.bind("<Leave>", lambda e: card.configure(fg_color=self.col_card_bg, border_width=0))
            card.bind("<Button-1>", lambda e: self.open_tool_form(target_view))

            # Ridotti i margini verticali (pady) per recuperare spazio prezioso
            lbl_icon = ctk.CTkLabel(card, text="📄", font=ctk.CTkFont(size=32))
            lbl_icon.pack(pady=(20, 5))
            lbl_icon.bind("<Button-1>", lambda e: self.open_tool_form(target_view))

            lbl_t = ctk.CTkLabel(card, text=titolo, font=ctk.CTkFont(size=13, weight="bold"), text_color=self.col_crema, wraplength=105, justify="center")
            lbl_t.pack(pady=5, padx=10)
            lbl_t.bind("<Button-1>", lambda e: self.open_tool_form(target_view))

            # Controllo esteso con "UN" per catturare "UNIQUEMENT" in francese
            is_italian_only = "SO" in sottotitolo or "ON" in sottotitolo or "NU" in sottotitolo or "UN" in sottotitolo

            # OTTIMIZZATO: wraplength ridotto a 115 per non toccare i bordi e rimosso il taglio inferiore
            lbl_s = ctk.CTkLabel(
                card, 
                text=sottotitolo, 
                font=ctk.CTkFont(size=10, weight="bold" if is_italian_only else "normal"), 
                text_color="#d9534f" if is_italian_only else "gray", 
                wraplength=115, 
                justify="center"
            )
            # expand=True permette alla label di prendersi lo spazio mancante senza troncare le lettere
            lbl_s.pack(pady=(5, 20), padx=5, fill="both", expand=True)
            lbl_s.bind("<Button-1>", lambda e: self.open_tool_form(target_view))


        crea_foglio_canvas(0, t["t2_title"], t["t2_sub"], "tool_2")
        crea_foglio_canvas(1, t["t3_title"], t["t3_sub"], "tool_3")
        crea_foglio_canvas(2, t["t4_title"], t["t4_sub"], "tool_4")
        crea_foglio_canvas(3, t["t1_title"], t["t1_sub"], "tool_1")

    def open_tool_form(self, target_view):
        self.current_view = target_view
        self.clear_frame()
        t = self.translations.get(self.lang, self.translations["EN"])

        self.btn_back = ctk.CTkButton(self, text=t["btn_back"], font=ctk.CTkFont(size=11, weight="bold"), fg_color="transparent", text_color=self.col_oro, hover_color="#2b2b2b", width=120, height=25, command=self.show_canvas_dashboard)
        self.btn_back.pack(anchor="w", padx=20, pady=(10, 5))

        self.form_frame = ctk.CTkFrame(self, fg_color=self.col_canvas_bg)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=(5, 5))

        if target_view == "tool_1":
            self.lbl_title_form = ctk.CTkLabel(self.form_frame, text=f"🇮🇹 {t['t1_title']}", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.col_crema)
            self.lbl_title_form.pack(anchor="w", padx=20, pady=(6, 2))
            
            self.lbl_sub_form = ctk.CTkLabel(self.form_frame, text=t["t1_sub"], font=ctk.CTkFont(size=11, weight="bold"), text_color="#d9534f")
            self.lbl_sub_form.pack(anchor="w", padx=20, pady=(0, 4))

            self.inner_switch = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            self.inner_switch.pack(anchor="w", padx=20, pady=(0, 4))
            self.calc_switch = ctk.CTkSwitch(self.inner_switch, text="", command=self.toggle_calc_mode, progress_color="#888888", fg_color="#4a4a4a", button_color="#dbdbdb", width=45)
            self.calc_switch.pack(side="left", padx=(0, 10))
            self.lbl_sw_dynamic = ctk.CTkLabel(self.inner_switch, text=t["mode_net"], font=ctk.CTkFont(size=11, slant="italic"), text_color="#b0b0b0")
            self.lbl_sw_dynamic.pack(side="left")

            self.crea_input_field(t["lbl_worker_t1"], "ent_1")
            self.crea_input_field(t["lbl_client_t1"], "ent_2")
            self.crea_input_field(t["lbl_amount_t1"], "ent_3", width=160)
            self.crea_input_field(t["lbl_details_t1"], "ent_4")

        elif target_view == "tool_2":
            self.lbl_title_form = ctk.CTkLabel(self.form_frame, text=f"🇺🇸 {t['t2_title']}", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.col_crema)
            self.lbl_title_form.pack(anchor="w", padx=20, pady=(10, 10))

            self.crea_input_field(t["lbl_worker_t2"], "ent_1")
            self.crea_input_field(t["lbl_client_t2"], "ent_2")
            self.crea_input_field(t["lbl_amount_t2"], "ent_3", width=250)
            self.crea_input_field(t["lbl_details_t2"], "ent_4")
        elif target_view == "tool_3":
            self.lbl_title_form = ctk.CTkLabel(self.form_frame, text=f"🌐 {t['t3_title']}", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.col_crema)
            self.lbl_title_form.pack(anchor="w", padx=20, pady=(10, 10))

            self.crea_input_field(t["lbl_worker_t3"], "ent_1")
            self.crea_input_field(t["lbl_client_t3"], "ent_2")
            self.crea_input_field(t["lbl_amount_t3"], "ent_3", width=200)
            self.crea_input_field(t["lbl_details_t3"], "ent_4")

        elif target_view == "tool_4":
            self.lbl_title_form = ctk.CTkLabel(self.form_frame, text=f"⚖️ {t['t4_title']}", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.col_crema)
            self.lbl_title_form.pack(anchor="w", padx=20, pady=(10, 10))

            self.crea_input_field(t["lbl_worker_t4"], "ent_1")
            self.crea_input_field(t["lbl_client_t4"], "ent_2")
            self.crea_input_field(t["lbl_amount_t4"], "ent_3", width=200)
            self.crea_input_field(t["lbl_details_t4"], "ent_4")

        self.bottom_btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_btn_frame.pack(fill="x", side="bottom", padx=20, pady=(5, 15))

        self.btn_execute = ctk.CTkButton(self.bottom_btn_frame, text=t["btn_generate"], font=ctk.CTkFont(size=13, weight="bold"), height=42, fg_color="#218838", hover_color="#28a745", text_color="white", command=self.generate_selected_pdf)
        self.btn_execute.pack(fill="x", expand=True)
    def crea_input_field(self, label_text, attr_name, width=None):
        lbl = ctk.CTkLabel(self.form_frame, text=label_text, font=ctk.CTkFont(size=11, weight="bold"), text_color="white", anchor="w", width=0, wraplength=500, justify="left")
        lbl.pack(fill="x", padx=20, pady=(2, 1))
        
        if width:
            entry = ctk.CTkEntry(self.form_frame, height=26, width=width, fg_color="#2b2b2b", text_color="white")
            entry.pack(anchor="w", padx=20, pady=(0, 4))
        else:
            # CORRETTO: Rimossi fill, padx e pady dall'inizializzazione di CTkEntry
            entry = ctk.CTkEntry(self.form_frame, height=26, fg_color="#2b2b2b", text_color="white")
            entry.pack(fill="x", padx=20, pady=(0, 4))
            
        setattr(self, attr_name, entry)


    def toggle_calc_mode(self):
        t = self.translations.get(self.lang, self.translations["EN"])
        if self.calc_switch.get() == 1:
            self.lbl_sw_dynamic.configure(text=t["mode_gross"])
        else:
            self.lbl_sw_dynamic.configure(text=t["mode_net"])
    def generate_selected_pdf(self):
        t = self.translations.get(self.lang, self.translations["EN"])
        
        d1 = self.ent_1.get().strip()
        d2 = self.ent_2.get().strip()
        d3 = self.ent_3.get().strip()
        d4 = self.ent_4.get().strip()

        if not d1 or not d2 or not d3 or not d4:
            messagebox.showwarning("PDFlash", t["err_fields"])
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("File PDF", "*.pdf")])
        if not output_path:
            return

        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            c.setLineWidth(1)

            styles = getSampleStyleSheet()
            style_left = ParagraphStyle('LegalLeft', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, alignment=TA_LEFT, textColor='black')
            style_justify = ParagraphStyle('LegalJustify', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, alignment=TA_JUSTIFY, textColor='black')
            style_italic = ParagraphStyle('LegalItalic', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, leading=14, alignment=TA_JUSTIFY, textColor='black')

            max_p_width = width - 110  

            if self.current_view == "tool_1":
                valore = float(d3.replace(",", "."))
                if self.calc_switch.get() == 0:
                    netto = valore
                    lordo = netto / 0.8
                    ritenuta = lordo * 0.20
                else:
                    lordo = valore
                    ritenuta = lordo * 0.20
                    netto = lordo - ritenuta

                marca_bollo = "Esente" if lordo <= 77.47 else "Imposta di bollo da 2,00 € assolta sull'originale"

                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 60, "RICEVUTA PER PRESTAZIONE OCCASIONALE")
                c.line(50, height - 70, width - 50, height - 70)
                
                current_y = height - 95
                
                c.setFont("Helvetica-Bold", 10)
                c.drawString(50, current_y, "Ricevuta emessa da:")
                current_y -= 15
                p1 = Paragraph(d1, style_left)
                _, p1_h = p1.wrap(max_p_width, 200)
                current_y -= p1_h
                p1.drawOn(c, 50, current_y)
                
                current_y -= 20
                c.setFont("Helvetica-Bold", 10)
                c.drawString(50, current_y, "Destinatario / Committente:")
                current_y -= 15
                p2 = Paragraph(d2, style_left)
                _, p2_h = p2.wrap(max_p_width, 200)
                current_y -= p2_h
                p2.drawOn(c, 50, current_y)

                current_y -= 20
                c.setFont("Helvetica-Bold", 10)
                c.drawString(50, current_y, "Descrizione della prestazione:")
                current_y -= 15
                testo_legale = "Corrispettivo per prestazioni di lavoro autonomo non esercitate abitualmente (Art. 67, DPR 917/1986)."
                if d4: testo_legale += f"<br/>Causale/Note: {d4}"
                p4 = Paragraph(testo_legale, style_italic)
                _, p4_h = p4.wrap(max_p_width, 300)
                current_y -= p4_h
                p4.drawOn(c, 50, current_y)

                current_y -= 25
                c.setLineWidth(0.5); c.line(50, current_y, width - 50, current_y)
                current_y -= 20
                c.setFont("Helvetica", 11); c.drawString(60, current_y, "COMPENSO LORDO:"); c.drawRightString(width - 60, current_y, f"{lordo:.2f} €")
                current_y -= 20
                c.drawString(60, current_y, "RITENUTA D'ACCONTO (20%):"); c.drawRightString(width - 60, current_y, f"- {ritenuta:.2f} €")
                current_y -= 15
                c.line(50, current_y, width - 50, current_y)
                current_y -= 20
                c.setFont("Helvetica-Bold", 11); c.drawString(60, current_y, "TOTALE NETTO DA CORRISPONDERE:"); c.drawRightString(width - 60, current_y, f"{netto:.2f} €")
                current_y -= 15
                c.line(50, current_y, width - 50, current_y)
                
                current_y -= 25
                c.setFont("Helvetica", 9)
                c.drawString(50, current_y, f"Marca da bollo: {marca_bollo}")
                current_y -= 15
                c.drawString(50, current_y, "Operazione fuori dal campo di applicazione dell'IVA ai sensi dell'Art. 5 del D.P.R. 633/1972.")
                firme_y = min(current_y - 60, height - 540)
            elif self.current_view == "tool_2":
                c.rect(40, 40, width - 80, height - 80, stroke=1, fill=0) 
                c.setFont("Helvetica-Bold", 15); c.drawString(55, height - 70, "SUBSTITUTE FORM W-8BEN")
                c.setFont("Helvetica", 10); c.drawString(55, height - 85, "Certificate of Foreign Status of Beneficial Owner for United States Tax Withholding")
                c.line(40, height - 95, width - 40, height - 95)
                
                current_y = height - 120
                c.setFont("Helvetica-Bold", 11); c.drawString(55, current_y, "Part I - Identification of Beneficial Owner")
                current_y -= 5
                c.line(55, current_y, width - 55, current_y)
                
                current_y -= 20
                txt_w8 = f"<b>1. Name of individual that is the beneficial owner:</b> {d1}<br/><br/>" \
                         f"<b>2. Permanent residence address (mailing address):</b> {d2}<br/><br/>" \
                         f"<b>3. Foreign tax identifying number (FTIN / Tax ID):</b> {d3}<br/><br/>" \
                         f"<b>4. Country of citizenship:</b> {d4}"
                p_w8 = Paragraph(txt_w8, style_left)
                _, p_w8_h = p_w8.wrap(max_p_width, 400)
                current_y -= p_w8_h
                p_w8.drawOn(c, 55, current_y)
                
                current_y -= 30
                c.line(40, current_y, width - 40, current_y)
                current_y -= 25
                c.setFont("Helvetica-Bold", 11); c.drawString(55, current_y, "Part II - Claim of Tax Treaty Benefits")
                current_y -= 5
                c.line(55, current_y, width - 55, current_y)
                
                current_y -= 25
                txt_treaty = f"The beneficial owner certifies that the individual is a resident of <u>{d4}</u> " \
                             f"within the meaning of the income tax treaty between the United States and that country."
                p_tr = Paragraph(txt_treaty, style_justify)
                _, p_tr_h = p_tr.wrap(max_p_width, 150)
                current_y -= p_tr_h
                p_tr.drawOn(c, 55, current_y)
                firme_y = min(current_y - 70, height - 540)

            elif self.current_view == "tool_3":
                c.rect(40, 40, width - 80, height - 80, stroke=1, fill=0)
                c.setFont("Helvetica-Bold", 15); c.drawString(55, height - 70, "MUTUAL NON-DISCLOSURE AGREEMENT")
                c.line(40, height - 85, width - 40, height - 85)
                
                current_y = height - 115
                txt_intro = f"This Confidentiality Agreement is entered into by and between the following active parties:<br/><br/>" \
                            f"<b>Disclosing Party:</b> {d1}<br/>" \
                            f"<b>Receiving Party:</b> {d2}"
                p_in = Paragraph(txt_intro, style_left)
                _, p_in_h = p_in.wrap(max_p_width, 250)
                current_y -= p_in_h
                p_in.drawOn(c, 55, current_y)
                
                current_y -= 30
                c.setFont("Helvetica-Bold", 11)
                c.drawString(55, current_y, "1. Scope of Protected Technology & Assets")
                current_y -= 15
                
                txt_scope = f"The disclosing party intends to share specific insights and digital assets defined as: <i>{d4}</i>"
                p_sc = Paragraph(txt_scope, style_justify)
                _, p_sc_height = p_sc.wrap(max_p_width, 300)
                current_y -= p_sc_height
                p_sc.drawOn(c, 55, current_y)
                
                current_y -= 30
                c.setFont("Helvetica-Bold", 11)
                c.drawString(55, current_y, "2. Binding Confidentiality Term")
                current_y -= 15
                
                txt_term = f"The obligations of non-disclosure shall remain bounded for a strict duration of: {d3}"
                p_te = Paragraph(txt_term, style_justify)
                _, p_te_height = p_te.wrap(max_p_width, 150)
                current_y -= p_te_height
                p_te.drawOn(c, 55, current_y)
                firme_y = min(current_y - 70, height - 540)
            elif self.current_view == "tool_4":
                c.rect(40, 40, width - 80, height - 80, stroke=1, fill=0)
                c.setFont("Helvetica-Bold", 15); c.drawString(55, height - 70, "FORMAL CEASE AND DESIST NOTICE")
                c.line(40, height - 85, width - 40, height - 85)
                
                current_y = height - 115
                c.setFont("Helvetica-Bold", 11); c.drawString(55, current_y, "LEGAL NOTICE REGARDING INTELLECTUAL PROPERTY")
                current_y -= 20
                txt_parties = f"<b>FROM COPYRIGHT OWNER:</b> {d1}<br/>" \
                              f"<b>TO ALLEGED INFRINGER ENTITY:</b> {d2}"
                p_pa = Paragraph(txt_parties, style_left)
                _, p_pa_h = p_pa.wrap(max_p_width, 200)
                current_y -= p_pa_h
                p_pa.drawOn(c, 55, current_y)
                
                current_y -= 30
                c.setFont("Helvetica-Bold", 11); c.drawString(55, current_y, "RE: DEMAND TO CEASE COPYRIGHT INFRINGEMENT IMMEDIATELY")
                current_y -= 20
                txt_demand = f"This letter serves as formal legal notice that your unauthorized actions violate protected work. " \
                             f"It has been officially documented that you are unlawfully exploiting the assets specified below:<br/>" \
                             f"<i>{d4}</i>"
                p_de = Paragraph(txt_demand, style_justify)
                _, p_de_h = p_de.wrap(max_p_width, 350)
                current_y -= p_de_h
                p_de.drawOn(c, 55, current_y)
                
                current_y -= 30
                c.setFont("Helvetica-Bold", 11); c.drawString(55, current_y, "Required Compliance Deadline")
                current_y -= 20
                txt_deadline = f"You are commanded to completely remove assets and reply within a deadline of: {d3}. " \
                               f"Failure to comply will force the owner to immediately escalate into judicial lawsuits."
                p_dl = Paragraph(txt_deadline, style_justify)
                _, p_dl_h = p_dl.wrap(max_p_width, 200)
                current_y -= p_dl_h
                p_dl.drawOn(c, 55, current_y)
                firme_y = min(current_y - 70, height - 540)

            c.setFont("Helvetica", 10)
            c.drawString(55, firme_y, "Executed on Date: ________________________")
            c.drawString(width - 290, firme_y, "Authorized Signature: ________________________")
            
            c.save()
            messagebox.showinfo("PDFlash", t["pop_success"])
            self.show_canvas_dashboard()  

        except Exception as e:
            messagebox.showerror("PDFlash", f"PDF Engine Error:\n{str(e)}")

    