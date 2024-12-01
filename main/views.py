from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context: dict[str, str] = {
        'title': 'Home',
        'content': 'Главная страница магазина - HOME',
        'list': ['first', 'second', 'third'],
        'dict': {'first': 'first', 'second': 'second'},
        'is_aunt': True
    }

    return render(request, 'main/index.html', context)


def about(request):
    return HttpResponse("about")
