import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
# Create your views here.

def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"<body>It is now %s.</body></html>' % now
    return HttpResponse(html)

def home(request):
    return render(request, 'home.html')