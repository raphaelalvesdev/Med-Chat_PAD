from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
from google.adk.tools.crewai_tool import CrewaiTool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client.http.models import Distance, VectorParams
from crewai_tools import QdrantVectorSearchTool
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

qdrant_tool = QdrantVectorSearchTool(
    qdrant_url = QDRANT_URL,
    qdrant_api_key = QDRANT_API_KEY,
    collection_name="demo_collection",
    embeddings=embeddings,
)
adk_qdrant_tool = CrewaiTool(
    name="qdrant_tool",
    description="A tool to search a Qdrant vector store.",
    tool=qdrant_tool,
)

