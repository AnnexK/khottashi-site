from django.shortcuts import render


def index(request):
    return render(request, 'pages/base.html')


def lorem(request):
    return render(request, 'pages/loremipsum.html')
