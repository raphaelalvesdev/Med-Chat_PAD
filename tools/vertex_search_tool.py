# tools/vertex_search_tool.py

# --- IMPORTAÇÕES ---
import vertexai
from google.adk.tools import VertexAiSearchTool

# --- CONFIGURAÇÃO DA FERRAMENTA ---
PROJECT_ID = "rag-pad"
LOCATION = "us-central1"
# O ID do seu Corpus que funcionou
CORPUS_ID = "2305843009213693952" 

# Inicializa o SDK do Vertex AI. É seguro chamar isso, pois a biblioteca
# lida com inicializações múltiplas.
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print("SDK do Vertex AI inicializado a partir do vertex_search_tool.py")
except Exception:
    print("SDK do Vertex AI já inicializado.")


# --- CRIAÇÃO E EXPORTAÇÃO DA FERRAMENTA ---

# Construindo o caminho completo que a ferramenta VertexAiSearchTool espera
data_store_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/dataStores/{CORPUS_ID}"

# Criamos a instância da ferramenta aqui e a deixamos pronta para ser importada
knowledge_search_tool = VertexAiSearchTool(data_store=data_store_path)

print(f"Instância da ferramenta 'knowledge_search_tool' criada e pronta para ser usada.")