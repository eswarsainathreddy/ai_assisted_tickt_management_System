from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import os

def retrieve(query, k=4):
    try:
        bi_encoder = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
        query_vector = bi_encoder.embed_query(query)
        client_url = os.getenv("QDRANT_CLIENT_URL", "http://localhost:6333")
        api_key = os.getenv("QDRANT_API_KEY")
        
        client = QdrantClient(url=client_url, api_key=api_key, timeout=2)

        results = client.query_points(
            collection_name="new_collection",
            query=query_vector,
            limit=k,
            with_payload=True
        )

        docs = []
        for point in results.points:
            if point.payload:
                docs.append(point.payload)

        if docs:
            return docs

    except Exception as e:
        print(f"[RAG Info] Qdrant retrieval fallback: {e}")

    # Default fallback SOP guidance for common query categories
    return [
        {
            "page_content": f"Standard Operating Procedure (SOP) for handling user inquiry: {query}",
            "metadata": {
                "answer": "Verify user account details, investigate transaction/log history, provide clear troubleshooting steps or process refund per policy."
            }
        }
    ]

