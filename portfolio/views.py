from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def startpage(request):
    return render(request, 'portfolio/portfolio.html')
