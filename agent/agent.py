from google.adk.agents import Agent# Import the tool
import yaml
import os
from dotenv import load_dotenv
from pathlib import Path
from tools.vertex_search_tool import knowledge_search_tool
load_dotenv()

cert_path = os.getenv('SSL_CERT_FILE')
if cert_path:
    print(f"SSL_CERT_FILE foi definido como: {cert_path}")
else:
    print("AVISO: SSL_CERT_FILE não foi encontrado no ambiente.")

script_dir = Path(__file__).parent 
yaml_path = script_dir / 'config' / 'agent_config' / 'agents.yaml'

print(f"Tentando carregar a configuração de: {yaml_path}") 

with open(yaml_path, 'r', encoding='utf-8') as file:
    agents = yaml.safe_load(file)

root_agent_config = agents['google_search_agent']
root_agent = Agent(
    name=root_agent_config['name'],
    description=root_agent_config['description'],
    instruction=root_agent_config['instruction'],
    model="gemini-2.0-flash-live-001",
    tools=[knowledge_search_tool]
)