from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.

def portada(request):
    return render(request, 'index.html')


def terminos_condiciones(request):
    """Vista para Términos y Condiciones"""
    return render(request, 'legal/terminos.html')


def politica_privacidad(request):
    """Vista para Política de Privacidad"""
    return render(request, 'legal/privacidad.html')


def faq(request):
    """Vista para Preguntas Frecuentes (FAQ)"""
    return render(request, 'faq.html')
