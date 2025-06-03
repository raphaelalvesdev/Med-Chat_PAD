from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def dashboard_page(request):
    return HttpResponse("<h1>Página do Dashboard (App Separada - Em Construção)</h1><p><a href='/chat/'>Nova Consulta</a></p>")