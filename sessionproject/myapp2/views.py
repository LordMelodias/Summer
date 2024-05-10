from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def setcookie(request):
    response = HttpResponse("Cookie Set")
    response.set_cookie("Rohit", "1056")
    return response

def getcookie(request):
    cookieid = request.COOKIES['Rohit']
    return HttpResponse("Cookie ID " + cookieid)
