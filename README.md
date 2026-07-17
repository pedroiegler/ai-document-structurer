# AI Document Structurer

Sistema que transforma texto livre em dados estruturados usando IA generativa.

## Sobre o Projeto

O **AI Document Structurer** recebe textos não estruturados (contratos, mensagens, descrições) e extrai automaticamente informações relevantes, convertendo-as em JSON estruturado.

Esse tipo de sistema é amplamente utilizado em empresas para automatizar a leitura e processamento de documentos.

## Fluxo do Sistema

texto livre → pré-processamento → IA (Gemini) → validação → JSON estruturado

**Exemplo:**

Entrada: João Silva firmou contrato com a empresa Tech Ltda em São Paulo, no dia 15 de março de 2024, pelo valor de R$ 50.000.

Saída:
```json
{
  "document_type": "contract",
  "entities": {
    "people": ["João Silva"],
    "organizations": ["Tech Ltda"],
    "dates": ["15 de março de 2024"],
    "values": ["R$ 50.000"],
    "locations": ["São Paulo"],
    "key_terms": ["contrato"]
  },
  "confidence": 1.0
}
```

## Arquitetura

Pipeline Architecture — sequência de etapas independentes onde a saída de uma é a entrada da próxima.

[Preprocessor] → [AI Extractor] → [Validator] → [Response]

## Stack

- **Python 3.13**
- **FastAPI** — API REST
- **Pydantic** — validação de schema e contrato de dados
- **LangChain** — orquestração do LLM
- **Google Gemini 2.5 Flash** — modelo de linguagem para extração
- **pytest** — testes automatizados
- **Docker** — containerização

## Estrutura do Projeto

ai-document-structurer/
├── app/
│   ├── api/
│   │   └── routes.py          # endpoints da API
│   ├── pipeline/
│   │   ├── preprocessor.py    # limpeza e normalização do texto
│   │   ├── extractor.py       # extração via LLM com Factory Pattern
│   │   └── validator.py       # validação e limpeza da saída
│   └── schemas/
│       └── extraction.py      # contrato de dados (entrada e saída)
├── tests/
│   ├── test_preprocessor.py
│   ├── test_validator.py
│   ├── test_schemas.py
│   └── test_api.py
├── main.py                    # inicialização da aplicação
├── Dockerfile
└── requirements.txt

## Padrões de Projeto Aplicados

- **Pipeline Pattern** — processamento sequencial em etapas isoladas
- **Factory Pattern** — seleção dinâmica de prompt por tipo de documento
- **Thin Controller** — camada HTTP sem lógica de negócio
- **Single Responsibility Principle** — cada componente com uma responsabilidade

## Como Rodar

### Local

```bash
# clone o repositório
git clone https://github.com/seu-usuario/ai-document-structurer.git
cd ai-document-structurer

# crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate

# instale as dependências
pip install -r requirements.txt

# configure as variáveis de ambiente
cp .env.example .env
# edite o .env com sua GEMINI_API_KEY

# rode a aplicação
uvicorn main:app --reload
```

### Docker

```bash
docker build -t ai-document-structurer .
docker run -p 8000:8000 --env-file .env ai-document-structurer
```

### Testes

```bash
pytest -v
```

## Endpoints

### `POST /api/v1/extract`

Extrai entidades de um texto.

**Request:**
```json
{
  "text": "seu texto aqui",
  "document_type": "contract"
}
```

**document_type:** `contract` | `message` | `description` | `unknown`

**Response:**
```json
{
  "document_type": "contract",
  "entities": {
    "people": [],
    "organizations": [],
    "dates": [],
    "values": [],
    "locations": [],
    "key_terms": []
  },
  "confidence": 0.83,
  "original_text": "seu texto aqui"
}
```

### `GET /api/v1/health`

Verifica se a API está rodando.

```json
{ "status": "ok" }
```

## Documentação Interativa

Com a aplicação rodando, acesse: http://localhost:8000/docs

## Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
GEMINI_API_KEY=sua-chave-aqui
```

Obtenha sua chave gratuita em: https://aistudio.google.com/apikey

## Testes

27 testes automatizados cobrindo:

- Testes unitários do preprocessor
- Testes unitários do validator
- Testes de validação de schema
- Testes E2E da API com mock do LLM