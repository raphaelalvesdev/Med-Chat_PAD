# BIA UFG: Med-Chat PAD

*Análise Preditiva para Apoio ao Diagnóstico Médico*

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Vertex_AI-orange.svg)](https://cloud.google.com/vertex-ai)
[![Framework](https://img.shields.io/badge/Framework-Google_ADK-green.svg)](https://google.github.io/adk-docs/)

## Descrição do Projeto

Este projeto implementa um agente de IA conversacional por voz, projetado para atuar como uma ferramenta de apoio à decisão para profissionais de saúde. O objetivo é otimizar a jornada do paciente e do médico antes da consulta, permitindo que o profissional realize uma "pré-consulta" interativa. O agente coleta informações sobre os sintomas do paciente e, utilizando uma arquitetura RAG (Retrieval-Augmented Generation), busca em uma base de dados histórica casos clínicos similares, apresentando os diagnósticos e padrões encontrados para enriquecer a análise do médico. Após a conversa, todo o conteúdo é salvo em um banco de dados, sendo possível a recuperação do conteúdo obtido na conversa.

## Arquitetura da Solução

O sistema é construído sobre a plataforma Google Cloud e utiliza uma arquitetura de agente de IA moderna.

1.  **Fonte de Dados:** Um arquivo CSV contendo dados estruturados de pacientes (sintomas, idade, fatores de risco, diagnóstico, etc.).
2.  **Tratamento de Dados (ETL):** Um notebook Jupyter (`data/process/...`) é usado para limpar os dados e, crucialmente, para criar uma coluna `narrativa`. Esta etapa de engenharia de features transforma os dados tabulares em texto semântico, que é a base para a busca de similaridade.
3.  **Base de Conhecimento RAG:** O arquivo de texto com as narrativas é ingerido pelo **Vertex AI RAG Engine** (anteriormente Vertex AI Search). O serviço automaticamente "vetoriza" cada narrativa usando o modelo de embedding **text-multilingual-embedding-002**, criando um banco de dados vetorial otimizado para busca semântica.
4.  **Cérebro do Agente (LLM):** O modelo **Gemini 2.0 Flash EXP** (ou superior) do Vertex AI é usado como o motor de raciocínio e geração de linguagem.
5.  **Orquestração (Framework):** O **Google Agent Development Kit (ADK)** é utilizado para estruturar o agente, gerenciar o estado da conversa e integrar as ferramentas.
6.  **Interface Final (Voicebot):** A arquitetura é projetada para ser o backend de um agente de voz, mas funciona com a interface de testes do ADK WEB.

## Estrutura do Projeto

A organização do projeto segue as melhores práticas de separação de conceitos:

```
.
├── agent/                  # Contém a lógica principal do agente (o "cérebro").
│   ├── agent.py
│   └── __init__.py
├── config/                 # Arquivos de configuração da personalidade do agente.
│   └── agent_config/
│       ├── agents.yaml
│       └── tasks.yaml
├── data/                   # Todos os dados e scripts de tratamento.
│   ├── data_final/         # Versões finais dos datasets, prontas para ingestão.
│   └── process/            # Notebooks Jupyter para limpeza e transformação.
├── tools/                  # Ferramentas que o agente pode usar (ex: busca RAG).
│   └── vertex_search_tool.py
├── .env                    # Arquivo para variáveis de ambiente (não versionado).
└── requirements.txt        
```

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar o agente em um ambiente de desenvolvimento local (recomendado: Debian ou WSL no Windows).

### Pré-requisitos
* Conta no Google Cloud com um projeto criado e faturamento ativado.
* [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install) instalado.
* Python 3.11 ou superior.
* `uv` (gerenciador de pacotes Python): `pip install uv`.

### 1. Configuração do Ambiente na Nuvem
- **Habilite a API do Vertex AI:** No seu projeto Google Cloud, navegue até o painel do Vertex AI e habilite as APIs recomendadas.
- **Crie um Bucket no Cloud Storage:** Crie um bucket para armazenar seus arquivos de dados.
- **Crie e Popule o Corpus RAG:**
    1.  Execute o notebook de tratamento de dados (`data/process/...`) para gerar o arquivo final `NARRATIVAS_PARA_VERTEX.txt`.
    2.  Faça o upload deste arquivo `.txt` para o seu bucket no Cloud Storage.
    3.  No Vertex AI, vá para **Mecanismo RAG** e crie um novo **Corpus**, apontando para o arquivo `.txt` que você subiu. Anote o **ID do Corpus**.

### 2. Configuração do Ambiente Local
1.  **Clone o Repositório:**
    ```bash
    git clone <url_do_repositorio>
    cd <pasta_do_projeto>
    ```
2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    uv venv
    source venv/bin/activate
    ```
3.  **Instale as Dependências:**
    ```bash
    # Se estiver usando requirements.txt
    uv pip install -r requirements.txt
    ```
4.  **Autentique-se no Google Cloud:**
    ```bash
    gcloud auth application-default login
    ```
5.  **Configure o Arquivo `.env`:**
    Crie um arquivo chamado `.env` na raiz do projeto e preencha com as informações do seu ambiente. Use o `.env.example` como base.

    **`.env.example`:**
    ```dotenv
    # Configurações do Google Cloud
    GOOGLE_CLOUD_PROJECT="seu-id-de-projeto-aqui"
    GOOGLE_CLOUD_LOCATION="us-central1"

    # ID do Corpus do Mecanismo RAG
    RAG_CORPUS_ID="seu-id-de-corpus-aqui"
    ```

### 3. Executando o Agente para Testes
Com o ambiente virtual ativado, execute o servidor de desenvolvimento do ADK:
```bash
adk web
```
Acesse `http://localhost:8000` no seu navegador para interagir com a interface de teste.

## Metodologia AGEMC

* 📌 **ASK:** Como podemos otimizar a jornada do paciente e do médico antes mesmo da consulta, utilizando um voicebot para realizar uma pré-consulta e fornecer informações relevantes ao profissional de saúde?
* 📌 **GET:** A base de dados primária é um arquivo CSV com dados anonimizados de SRAG (Síndrome Respiratória Aguda Grave) em idosos, contendo informações de sintomas, comorbidades e diagnósticos.
* 📌 **EXPLORE:** O tratamento de dados foi realizado em um notebook Jupyter. A principal etapa de engenharia de features foi a criação de uma coluna `narrativa`, que converte os dados estruturados (binários e categóricos) em sentenças de linguagem natural para permitir a busca semântica. Colunas irrelevantes (`SG_UF`, `CLASSI_FIN`) foram removidas.
* 📌 **MODEL:** A solução utiliza uma arquitetura RAG (Retrieval-Augmented Generation). O backend de busca é o **Vertex AI RAG Engine**, que indexa as narrativas. O cérebro do agente é o **Gemini 2.0 Flash Exp** (ou superior), e a orquestração do fluxo conversacional e do uso de ferramentas é gerenciada pelo **Google Agent Development Kit (ADK)**.
* 📌 **COMMUNICATE:** O objetivo final é uma interface de voz. O agente foi instruído (via prompt de sistema no `agents.yaml`) a ser conciso e a resumir os achados, atuando como uma ferramenta de apoio à decisão em vez de fornecer um diagnóstico. A implantação final recomendada é no **Google Cloud Run** para escalabilidade e integração com APIs de Speech-to-Text e Text-to-Speech.
