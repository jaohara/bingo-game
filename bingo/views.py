from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return HttpResponse("Do I remember how this works?")


