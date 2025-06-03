# chat/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Para simplificar o AJAX POST neste exemplo
from .langchain_service import generate_response

def chat_page(request):
    """
    Renderiza a página HTML principal do chat.
    """
    return render(request, 'chat/chat_interface.html')

@csrf_exempt # Importante para requisições POST via AJAX sem o token CSRF configurado no JS.
             # Em produção, configure o token CSRF corretamente no seu JavaScript.
def chatbot_api(request):
    """
    API endpoint para interagir com o chatbot.
    Recebe uma mensagem do usuário e retorna a resposta do bot.
    """
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if not user_message:
            return JsonResponse({'error': 'Mensagem não pode ser vazia.'}, status=400)

        # Garante que a sessão exista para obter um session_id
        if not request.session.session_key:
            request.session.create() # Cria uma sessão se não houver uma
        session_id = request.session.session_key

        bot_response = generate_response(session_id, user_message)
        return JsonResponse({'response': bot_response})

    return JsonResponse({'error': 'Método GET não é permitido para este endpoint.'}, status=405)