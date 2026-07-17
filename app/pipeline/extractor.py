import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.extraction import DocumentType, ExtractedEntities

load_dotenv()


EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
            You are a specialist in extracting structured entities from documents.

            Your task is to analyze the provided text and extract the following entities:

            - people: full names of individuals mentioned
            - organizations: names of companies, institutions, or organizations
            - dates: any dates mentioned, in their original format
            - values: monetary values, percentages, or quantities
            - locations: geographic locations, cities, countries, or addresses
            - key_terms: relevant technical or domain-specific terms

            Rules you must follow:
            - Extract ONLY information explicitly present in the text
            - Do NOT invent or infer information that is not clearly stated
            - If an entity type is not found, return an empty list
            - Normalize people names to their full form when possible
        """
    ),
    (
        "human", 
        "Extract all entities from the following text:\n\n{text}"
    )
])

CONTRACT_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
            """
            You are a specialist in extracting structured entities from legal contracts.

            Focus especially on:
            - people: all parties involved (individuals)
            - organizations: all parties involved (companies)
            - dates: signing date, deadlines, validity periods
            - values: monetary amounts, percentages, penalties
            - locations: jurisdiction, place of signing
            - key_terms: obligations, rights, clauses, penalties

            Rules:
            - Extract ONLY information explicitly present in the text
            - Do NOT invent or infer information
            - If an entity type is not found, return an empty list
        """
    ),
    (
        "human", 
        "Extract all entities from the following contract:\n\n{text}"
    )
])

MESSAGE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
            You are a specialist in extracting structured entities from messages and communications.

            Focus especially on:
            - people: sender, recipients, mentioned individuals
            - organizations: mentioned companies or groups
            - dates: dates and times mentioned
            - values: any quantities or amounts mentioned
            - locations: places mentioned
            - key_terms: main topics, actions requested, sentiment indicators

            Rules:
            - Extract ONLY information explicitly present in the text
            - Do NOT invent or infer information
            - If an entity type is not found, return an empty list
        """
    ),
    (
        "human", 
        "Extract all entities from the following message:\n\n{text}"
    )
])

def _get_prompt_for_document_type(document_type: DocumentType) -> ChatPromptTemplate:
    """
    Factory function: returns the appropriate prompt for the given document type.
    """
    prompt_map = {
        DocumentType.CONTRACT: CONTRACT_PROMPT,
        DocumentType.MESSAGE: MESSAGE_PROMPT,
        DocumentType.DESCRIPTION: EXTRACTION_PROMPT,
        DocumentType.UNKNOWN: EXTRACTION_PROMPT,
    }
    return prompt_map.get(document_type, EXTRACTION_PROMPT)

class AIExtractor:
    def __init__(self, model: str = "gemini-2.5-flash", temperature: float = 0.0):
        self._llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GEMINI_API_KEY"),
        )

    def extract(self, text: str, document_type: DocumentType = DocumentType.UNKNOWN) -> ExtractedEntities:
        """
        Extract structured entities using a prompt specific to the document type.
        """
        prompt = _get_prompt_for_document_type(document_type)
        chain = prompt | self._llm.with_structured_output(ExtractedEntities)

        return chain.invoke({"text": text})
