import os
from PIL import Image, ImageDraw

def genera_monogramma_oro_3d():
    # Risoluzione premium per Windows (256x256 pixel)
    size = (256, 256)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 1. DISEGNO DELLO SQUIRCLE (Sfondo grigio antracite scuro opaco)
    sfondo_colore = "#1e1e1e"
    raggio = 55  
    draw.rounded_rectangle((10, 10, 246, 246), radius=raggio, fill=sfondo_colore)
    
    # Colori oro reali presi dai tuoi componenti della UI
    oro_brillante = "#FFEFCB"  # Colore testo badge
    oro_scuro = "#91733E"      # Colore hover tasto upgrade
    
    # 2. LATO SINISTRO DELLA "F" (In ombra - Oro Scuro)
    faccia_sinistra = [
        (85, 210),   # Base inferiore del gambo
        (120, 210),  # Larghezza del gambo
        (120, 140),  # Salita verso l'aletta inferiore
        (165, 140),  # Fine aletta inferiore
        (165, 110),  # Spessore aletta inferiore
        (120, 110),  # Rientro verso il gambo centrale
        (120, 85),   # Salita
        (140, 55),   # Asse centrale di giunzione freccia
        (85, 55),    # Chiusura testa
    ]
    draw.polygon(faccia_sinistra, fill=oro_scuro)
    
    # 3. LATO DESTRO DELLA "F" CON LA FRECCIA (Illuminato - Oro Brillante)
    faccia_destra = [
        (120, 110),  # Punto di aggancio interno
        (120, 85),   # Salita verso l'aletta superiore dinamica
        (155, 85),   # Inizio della freccia
        (155, 105),  # Base della punta della freccia (sporgenza destra)
        (195, 70),   # PUNTA DELLA FRECCIA RIVOLTA AL FUTURO
        (140, 35),   # Base sinistra della punta della freccia
        (140, 55),   # Asse centrale di giunzione freccia
    ]
    draw.polygon(faccia_destra, fill=oro_brillante)
    
    # Salva il file sovrascrivendo l'icona precedente
    icon_path = "icona.ico"
    image.save(icon_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
    print("🏆 Icona 'F-Futuro Gold Edition' generata con successo nella tua cartella!")

if __name__ == "__main__":
    genera_monogramma_oro_3d()
