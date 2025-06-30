from langchain_openai import ChatOpenAI  # Offizieller OpenAI-Adapter
from langchain_core.prompts import ChatPromptTemplate  # Modernes Prompt-Handling
from langchain_core.output_parsers import StrOutputParser  # Textausgabe
from langchain_core.runnables import RunnablePassthrough
import os

def analyze_contract(text: str) -> str:
    """
    Analysiert Vertragstext mit GPT-3.5-turbo (LangChain 0.3.x kompatibel).
    
    Args:
        text: Zu analysierender Text (max. 15.000 Zeichen)
    
    Returns:
        Formatierte Analyse als Markdown-String
    
    Raises:
        RuntimeError: Bei API-Fehlern oder Kontingentproblemen
    """
    # Modernes Prompt-Template mit Systemanweisung
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Sie sind ein juristischer Experte. Analysieren Sie:
1. Unklare Formulierungen (mit Artikelangaben)
2. Top-3-Risiken (Bewertung 1-10)
3. Konkrete Änderungsvorschläge

Halten Sie sich strikt an dieses Format:"""),
        ("human", "{text}")
    ])

    try:
        # Chain mit moderner Syntax (| Operator)
        chain = (
            {"text": RunnablePassthrough()} 
            | prompt
            | ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.3,
                max_tokens=2000,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            | StrOutputParser()
        )
        
        return chain.invoke(text[:15000])
        
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower():
            raise RuntimeError("API-Kontingent erschöpft. Bitte OpenAI-Dashboard prüfen.")
        raise RuntimeError(f"Analyse fehlgeschlagen: {error_msg}")

# Test
if __name__ == "__main__":
    test_text = "Der Vermieter haftet nur für Vorsatz."
    print(analyze_contract(test_text))