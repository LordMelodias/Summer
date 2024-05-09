from django import forms

# create form 
class employee(forms.Form):
    username = forms.CharField(label="Enter Username",max_length=20)
    email = forms.EmailField(label="Enter Email")
    password = forms.CharField(label="Enter Password",max_length=10)
    file = forms.FileField()
    