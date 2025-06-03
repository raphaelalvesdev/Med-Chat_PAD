from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from django.conf import settings

session_chains = {}

def get_conversation_chain(session_id: str):
    """
    Cria ou recupera uma cadeia de conversação para uma sessão específica.
    A memória da conversa será mantida por session_id.
    """
    if session_id in session_chains:
        return session_chains[session_id]
    
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.OPENAI_MODEL,
        temperature= 0.7,
    )

    memory = ConversationBufferMemory()

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    session_chains[session_id] = chain
    return chain

def generate_response(session_id: str, user_message: str) -> str:
    """
    Gera uma resposta do chatbot para a mensagem do usuário usando a cadeia da sessão.
    """
    chain = get_conversation_chain(session_id)
    try:
        # Langchain mudou a forma de invocar chains. predict ainda funciona para casos simples.
        # Para estruturas de entrada/saída mais complexas, use .invoke()
        # response = chain.invoke({"input": user_message})
        # bot_reply = response.get("response", "Desculpe, não entendi.")
        bot_reply = chain.predict(input=user_message)
    except Exception as e:
        print(f"Erro ao chamar Langchain: {e}")
        bot_reply = "Desculpe, ocorreu um erro ao processar sua mensagem."
    return bot_reply