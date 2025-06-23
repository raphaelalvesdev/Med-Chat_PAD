# tools/vertex_search_tool.py
# Responsável por criar uma instância configurada da ferramenta de busca RAG.

from google.adk.tools.retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- 1. CONFIGURAÇÃO DA FERRAMENTA ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
RAG_CORPUS_ID = os.getenv("RAG_CORPUS_ID")

# --- 2. CRIAÇÃO E EXPORTAÇÃO DA FERRAMENTA ---

# Constrói o caminho completo para o nosso Corpus
corpus_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{RAG_CORPUS_ID}"

# Criamos a instância da ferramenta. Ela será usada no agent.py.
knowledge_search_tool = VertexAiRagRetrieval(
    name="busca_em_registros_medicos_historicos",
    description="Use esta ferramenta para buscar e encontrar informações sobre casos de pacientes, sintomas e diagnósticos em uma base de dados de prontuários.",
    rag_resources=[
        rag.RagResource(
            rag_corpus=corpus_path,
        )
    ]
)

print(f"Ferramenta 'knowledge_search_tool' configurada e pronta para ser importada.")