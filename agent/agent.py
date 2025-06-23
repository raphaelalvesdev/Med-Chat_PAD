# agent.py - Versão Final que carrega configurações do YAML

# --- 1. IMPORTAÇÕES ---
import vertexai
from vertexai.generative_models import GenerativeModel
from google.adk.agents import Agent
import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Importamos a instância da ferramenta já pronta
from tools.vertex_search_tool import knowledge_search_tool

# --- 2. CONFIGURAÇÃO E INICIALIZAÇÃO ---
load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

# A CHAVE NO ARQUIVO YAML QUE QUEREMOS USAR PARA ESTE AGENTE
AGENT_CONFIG_KEY = "assistente_medico" 

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION)

# --- 3. CARREGAMENTO DAS CONFIGURAÇÕES DO ARQUIVO YAML ---
print(f"Carregando a configuração para o agente '{AGENT_CONFIG_KEY}' do arquivo YAML...")
try:
    # Lógica para encontrar o arquivo config na raiz do projeto
    project_root = Path(__file__).parent.parent
    yaml_path = project_root / 'config' / 'agent_config' / 'agents.yaml'
    
    with open(yaml_path, 'r', encoding='utf-8') as file:
        agents_config_yaml = yaml.safe_load(file)
    
    # Pega a configuração específica do nosso agente usando a chave
    agent_specific_config = agents_config_yaml[AGENT_CONFIG_KEY]
    print("Configuração carregada com sucesso.")
except Exception as e:
    print(f"ERRO ao carregar o YAML: {e}. O agente não será criado corretamente.")
    # Interrompe a execução se o YAML não puder ser lido
    sys.exit()

# --- 5. DEFINIÇÃO DO AGENTE PRINCIPAL ---
# Criamos o agente usando os valores que carregamos do arquivo YAML
root_agent = Agent(
    name=agent_specific_config['name'],
    description=agent_specific_config['description'],
    instruction=agent_specific_config['instruction'],
    model="gemini-2.0-flash-exp",
    tools=[knowledge_search_tool]
)

print(f"Agente '{root_agent.name}' criado e pronto para execução com base na configuração do YAML.")