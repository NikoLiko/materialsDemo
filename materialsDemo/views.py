from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pymongo
import json

def index(request):
    return render(request,"index.html")
