from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_user(request):
    return HttpResponse("Hello, users!")