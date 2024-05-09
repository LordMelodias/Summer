from django.shortcuts import render
from django.http import HttpResponse
from upload.functions import handle_uploaded_file
from upload.forms import employee  # Renaming the form class

def index(request):
    if request.method =='POST':
        form = employee(request.POST, request.FILES)  # Renaming the form instance
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("File Uploaded Successfully")
    else:
        form = employee()  # Creating a new form instance for GET requests

    return render(request, "index.html", {'form': form})  # Fixed the typo here: 'form', employee -> 'form': form
