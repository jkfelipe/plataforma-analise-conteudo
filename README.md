# Plataforma de Análise de Conteúdo

Este repositório contém uma API desenvolvida com **FastAPI** para análise de sentimentos de textos, utilizando as bibliotecas **TextBlob** e **VADER**. A API permite a detecção do idioma do texto, tradução para inglês (se necessário) e armazenamento das análises no **MongoDB**.

## Funcionalidades
- **Detecção de idioma** do texto enviado.
- **Tradução automática** para inglês caso o texto não esteja nesse idioma.
- **Análise de sentimentos** com **TextBlob** e **VADER**.
- **Armazenamento** das análises no **MongoDB**.

## Tecnologias Utilizadas
- **FastAPI**: Framework para desenvolvimento da API.
- **MongoDB**: Banco de dados NoSQL para armazenamento das análises.
- **Motor (Motor AsyncIO)**: Cliente assíncrono para conexão com o MongoDB.
- **TextBlob**: Biblioteca para processamento de linguagem natural e análise de sentimentos.
- **VADER (nltk.sentiment)**: Análise de sentimentos otimizada para textos curtos.
- **Googletrans**: API para tradução de idiomas.

## Requisitos
Antes de executar a API, certifique-se de ter instalado:
- **Python 3.8+**
- **MongoDB** rodando localmente ou em um servidor remoto.

### Instalação das Dependências
```bash
pip install fastapi uvicorn motor googletrans==4.0.0-rc1 textblob nltk
```

### Executando a API
Defina a variável de ambiente **MONGO_URI** ou utilize o padrão **mongodb://localhost:27017/analisador**.

Para iniciar a API, execute:
```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000/`.

## Endpoints
### Testar a API
```http
GET /
```
**Resposta:**
```json
{
    "message": "API está rodando!"
}
```

### Testar conexão com MongoDB
```http
GET /test-db
```
**Resposta esperada:**
```json
{
    "message": "Conexão com MongoDB bem-sucedida!"
}
```

### Análise de Sentimentos com TextBlob
```http
POST /npl-textblob
```
**Corpo da requisição:**
```json
{
    "texto": "Estou muito feliz hoje!"
}
```
**Resposta esperada:**
```json
{
    "texto": "Estou muito feliz hoje!",
    "idioma_detectado": "pt",
    "english": "I am very happy today!",
    "sentimento": "positive",
    "subjectividade": 0.5,
    "polaridade": 0.9
}
```

### Análise de Sentimentos com VADER
```http
POST /npl-vader
```
**Corpo da requisição:**
```json
{
    "texto": "Estou muito feliz hoje!"
}
```
**Resposta esperada:**
```json
{
    "texto": "Estou muito feliz hoje!",
    "idioma_detectado": "pt",
    "english": "I am very happy today!",
    "compound": 0.85,
    "neg": 0.0,
    "neu": 0.3,
    "pos": 0.7,
    "sentimento": "positive"
}
```

## Contribuição
Se você deseja contribuir, siga estas etapas:
1. **Fork** o repositório.
2. Crie um **branch** para sua funcionalidade (`git checkout -b minha-nova-feature`).
3. **Commit** suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. **Push** para o branch (`git push origin minha-nova-feature`).
5. Abra um **Pull Request**.

