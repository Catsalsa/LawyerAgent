import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from utils.pdf_reader import extract_text_from_pdf
from utils.analysis import analyze_contract

# Lade Umgebungsvariablen
load_dotenv()

def main():
    try:
        # 0. Vorab-Prüfungen
        if not os.getenv("OPENAI_API_KEY"):
            print("\n❌ OPENAI_API_KEY nicht gefunden in .env Datei")
            print("ℹ️  Tipp: Erstellen Sie eine .env Datei mit: OPENAI_API_KEY=ihr_key_ohne_anführungszeichen")
            return

        # 1. Pfade konfigurieren
        PROJECT_ROOT = Path(__file__).parent.absolute()
        print(f"\n⚖️ LawyerAgent gestartet in: {PROJECT_ROOT}")

        # 2. PDF-Datei prüfen
        pdf_path = PROJECT_ROOT / "documents/beispiel.pdf"
        
        if not pdf_path.exists():
            print("\n⚠️  PDF nicht gefunden. Bitte legen Sie eine Datei namens:")
            print(f"   '{pdf_path}'")
            print("   Alternativ können Sie den Dateinamen in app.py anpassen")
            return
            
        if not pdf_path.suffix.lower() == '.pdf':
            print(f"\n❌ Fehler: Datei '{pdf_path.name}' ist keine PDF-Datei")
            return

        # 3. PDF verarbeiten
        print("\n🔍 Lese und analysiere Vertrag...")
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            raise ValueError("PDF enthält keinen lesbaren Text")

        # 4. Analyse durchführen
        analysis = analyze_contract(text)

        # 5. Ergebnisse anzeigen
        print("\n" + "═" * 60)
        print("📋 Analyseergebnis".center(60))
        print("═" * 60)
        print(analysis)
        print("═" * 60)
        print(f"\n✅ Analyse erfolgreich abgeschlossen für: {pdf_path.name}\n")

    except Exception as e:
        print(f"\n❌ Kritischer Fehler: {str(e)}")
        if "OPENAI_API_KEY" in str(e):
            print("ℹ️  Lösung: .env Datei mit API-Key erstellen")
        elif "ChatCompletion" in str(e):
            print("ℹ️  Lösung: Führen Sie aus -> pip install --upgrade langchain-community openai")
        elif "PDF" in str(e):
            print("ℹ️  Lösung: Überprüfen Sie die PDF-Datei auf Lesbarkeit")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())

 