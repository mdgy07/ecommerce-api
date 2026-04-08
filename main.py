import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Charger les variables secrètes
load_dotenv()

app = FastAPI(title="E-commerce Data Extractor Pro")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Définition de ce que l'utilisateur DOIT envoyer
class ExtractionRequest(BaseModel):
    description: str

@app.post("/extract")
async def extract_data(request: ExtractionRequest):
    if not request.description:
        raise HTTPException(status_code=400, detail="La description est vide")
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant e-commerce. Extrais les données en JSON : produit, marque, prix, etat, devise."
                },
                {"role": "user", "content": request.description}
            ],
            model="llama3-8b-8192",
            response_format={"type": "json_object"}
        )
        return {"success": True, "data": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))