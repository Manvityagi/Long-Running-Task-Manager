from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')
def getFile(request, filename):
    return render(request,f'{filename}.csv')
