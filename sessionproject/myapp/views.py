from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def setsession(request):
    request.session['ename'] = "Rohit"
    request.session['eemail'] = "rohitchauhan9880@gmail.com"
    return HttpResponse("Session is Set")

def getsession(request):
    empname = request.session['ename']
    empemail = request.session['eemail']
    return HttpResponse(empname + "  " + empemail)


