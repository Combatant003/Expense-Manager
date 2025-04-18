from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdf_parser import extract_text_from_pdf
from insight_engine import get_insights
from chart_generator import get_chart_data

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_pdf(contents)

    insights = get_insights(text)
    charts = get_chart_data(text)

    return {
        "insights": insights,
        "charts": charts
    }
