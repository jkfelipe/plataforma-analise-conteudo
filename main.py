from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
import datetime  # Mantemos datetime de forma otimizada
from googletrans import Translator
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Criar a aplicação FastAPI
app = FastAPI()

# Baixar recursos do NLTK necessários
nltk.download('vader_lexicon')

# Modelo de entrada para a API
class TextoEntrada(BaseModel):
    texto: str

# Iniciar o tradutor e o analisador de sentimentos VADER
tradutor = Translator()
sia = SentimentIntensityAnalyzer()

# Conectar ao MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/analisador")
client = AsyncIOMotorClient(MONGO_URI)
db = client.analisador

# Endpoint raiz
@app.get("/")
def home():
    return {"message": "API está rodando!"}

# Endpoint para testar a conexão com MongoDB
@app.get("/test-db")
async def test_db():
    try:
        # Testar conexão com MongoDB
        await db.command("ping")
        return {"message": "Conexão com MongoDB bem-sucedida!"}
    except Exception as e:
        return {"error": str(e)}

# Função obter sentimento e salvar no MongoDB
@app.post("/npl-textblob")
async def analisar_sentimento(dados: TextoEntrada):
    modelo = 'textblob'
    try:
        # Detectar idioma
        idioma_detectado = tradutor.detect(dados.texto).lang

        # Traduzir se necessário
        if idioma_detectado != "en":            
            texto_traduzido = tradutor.translate(dados.texto, dest="en").text
        else:
            texto_traduzido = dados.texto

        # Usar análise de sentimento do TextBlob apenas se for necessário
        polaridade = TextBlob(texto_traduzido).sentiment.polarity
        subjectividade = TextBlob(texto_traduzido).sentiment.subjectivity

        # Definir o sentimento
        if polaridade > 0:
            sentimento = "positive"
        elif polaridade < 0:
            sentimento = "negative"
        else:
            sentimento = "neutral"

        # Salvar no MongoDB
        await db.analiseSentimento.insert_one({
            "texto": dados.texto,
            "idioma_detectado": idioma_detectado,
            "traducao": texto_traduzido,
            "polaridade": polaridade,
            "subjectividade": subjectividade,
            "sentimento": sentimento,
            "modelo": modelo,
            "data": datetime.datetime.now()
        })

        return {
            "texto": dados.texto,
            "idioma_detectado": idioma_detectado,
            "english": texto_traduzido,
            "sentimento": sentimento,
            "subjectividade": subjectividade,
            "polaridade": polaridade
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para análise de sentimentos com VADER
@app.post("/npl-vader")
async def analisar_sentimento_vader(dados: TextoEntrada):
    modelo = 'vader'
    try:
        # Detectar idioma
        idioma_detectado = tradutor.detect(dados.texto).lang

        # Traduzir se necessário
        if idioma_detectado != "en":
            texto_traduzido = tradutor.translate(dados.texto, dest="en").text
        else:
            texto_traduzido = dados.texto

        # Aplicar análise de sentimentos VADER
        scores = sia.polarity_scores(texto_traduzido)
        compound = scores['compound']
        neg = scores['neg']
        neu = scores['neu']
        pos = scores['pos']

        # Definir o sentimento
        if compound >= 0.05:
            sentimento = "positive"
        elif compound <= -0.05:
            sentimento = "negative"
        else:
            sentimento = "neutral"

        # Salvar no MongoDB
        await db.analiseSentimento.insert_one({
            "texto": dados.texto,
            "idioma_detectado": idioma_detectado,
            "traducao": texto_traduzido,
            "compound": compound,
            "neg": neg,
            "neu": neu,
            "pos": pos,
            "sentimento": sentimento,
            "modelo": modelo,
            "data": datetime.datetime.now()
        })

        return {
            "texto": dados.texto,
            "idioma_detectado": idioma_detectado,
            "english": texto_traduzido,
            "compound": compound,
            "neg": neg,
            "neu": neu,
            "pos": pos,
            "sentimento": sentimento,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))