from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
from django.shortcuts import render


def portada(request):
    return render(request, 'index.html')
