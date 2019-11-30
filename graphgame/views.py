from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.


def game(request):
    if request.method == 'POST':
        print(request.body)
    else:
        return render(request, 'graphgame/index.html')
