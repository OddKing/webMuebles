from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def vista_base(request):
    return render(request, 'base.html')
