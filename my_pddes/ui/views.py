from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login 
from django.contrib import messages

# Create your views here.

def home_view(request):

    return render(request, "index(home).html")

def about_view(request):
    return render(request, "about.html")

def help_view(request):
    return render(request, "help.html")

def contact_view(request):
    return render(request, "contact.html")

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("homepage")
        messages.error(request, "Registration unsuccessful. invalid info")
    form = NewUserForm()
    return render (request=request, template_name="registration/signup.html", context={"register_form":form})