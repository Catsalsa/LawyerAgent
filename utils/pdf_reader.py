from PyPDF2 import PdfReader
from pathlib import Path

def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extrahiert Text aus einer PDF-Datei
    
    Args:
        pdf_path: Pfad zur PDF-Datei (als String oder Path-Objekt)
    
    Returns:
        Extrahierten Text als String
    
    Raises:
        RuntimeError: Wenn die PDF nicht gelesen werden kann
    """
    try:
        pdf_path = Path(pdf_path) if isinstance(pdf_path, str) else pdf_path
        
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = []
            for i, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                text.append(f"Seite {i}:\n{page_text}" if page_text else f"Seite {i}: Kein Text")
            return "\n\n".join(text)
    except Exception as e:
        raise RuntimeError(f"PDF konnte nicht gelesen werden: {str(e)}")