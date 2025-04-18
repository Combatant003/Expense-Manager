from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Analyze the following expense text:

{text}

Return your result strictly in the following JSON format:

{{
  "summary": "short textual insight",
  "categories": [
    {{"category": "Food", "amount": 500}},
    {{"category": "Transport", "amount": 200}},
    ...
  ],
  "monthly_trend": [
    {{"month": "Jan", "amount": 1200}},
    {{"month": "Feb", "amount": 1000}},
    ...
  ]
}}

Only return the JSON. Do not add any explanation.
"""
)

def get_insights(text: str) -> str:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents([Document(page_content=text)])

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embedding=embeddings)
    retriever = db.as_retriever()

    llm = Ollama(model="llama3")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    query = "Summarize this expense data. What are the top categories and trends?"
    result = qa.run(query)
    return result