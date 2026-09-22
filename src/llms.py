from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.state import IncidentClassification

load_dotenv()

gemini_llm=ChatGoogleGenerativeAI(model="gemini-3.6-flash")
llm=ChatGroq(model="openai/gpt-oss-20b")

Incident_classifier=gemini_llm.with_structured_output(IncidentClassification)
