def handle_uploaded_file(f):  
    with open('upload/static/uploads/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)