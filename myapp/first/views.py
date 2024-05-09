from django.shortcuts import render

# Create your views here.

# Trial 
def index(request):
    name = {'admin':'Rohit', 'age':'20'}
    return render(request, 'index.html', name)

def about(request):
    return render(request, 'about.html')
