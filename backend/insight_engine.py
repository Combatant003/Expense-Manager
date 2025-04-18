import re
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

def extract_json_from_text(raw_text: str) -> dict:
    try:
        # find first { and last } to extract JSON block
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            json_text = match.group()
            return json.loads(json_text)
        else:
            raise ValueError("No JSON block found in output.")
    except Exception as e:
        print(f"Failed to extract JSON: {e}")
        return {
            "summary": "Could not parse LLM output properly.",
            "categories": [],
            "monthly_trend": []
        }

def get_insights(text: str) -> dict:
    if not text.strip():
        print("Warning: Empty text extracted from PDF.")
        return {
            "summary": "No text extracted from uploaded PDF.",
            "categories": [],
            "monthly_trend": []
        }

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents([Document(page_content=text)])

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embedding=embeddings)
    retriever = db.as_retriever()

    llm = OllamaLLM(model="deepseek-r1:8b")
    prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    You are an intelligent expense analyzer.

    Given the following extracted text from an expense report:

    {text}

    Please do the following:

    1. Analyze the expense text.
    2. Identify and list the top expense categories with their estimated total amounts.
    3. Identify monthly trends (total spending per month).

    Finally, respond STRICTLY in the following JSON format:

    {{
      "summary": "<high-level insights>",
      "categories": [
        {{"category": "CategoryName", "amount": Amount}},
        ...
      ],
      "monthly_trend": [
        {{"month": "MonthName", "amount": Amount}},
        ...
      ]
    }}

    Rules:
    - Only output valid JSON without any extra explanation.
    - Estimate values as accurately as possible from the provided text.
    """
    )

    chain = prompt | llm

    try:
        raw_response = chain.invoke({"text": text[:3000]})
        print(raw_response)
        if isinstance(raw_response, dict):
            return raw_response
        return extract_json_from_text(raw_response)
    except Exception as e:
        print("LLM output parsing error:", e)
        return {
            "summary": "Failed to parse LLM output.",
            "categories": [],
            "monthly_trend": []
        }