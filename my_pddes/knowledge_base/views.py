from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import Symptoms, Diagnosis, System_rules
# Create your views here.
def disorder_info_view(request):
    if request.method == "POST":

        form = Symptoms(request.POST)
        form2 = Diagnosis(request.POST)
        form3 = System_rules(request.POST)
        if form.is_valid():
            kb_data = form.save()
            messages.success(request, "Data added to the Knowledge base Successfully")
            form = Symptoms()
        
        elif form2.is_valid():
            kb_data = form2.save()
            messages.success(request, "Data added to the Knowledge base Successfully")
            form2 = Diagnosis()

        elif form3.is_valid():
            kb_data = form3.save()
            messages.success(request, "Data added to the Knowledge base Successfully")
            form3 = System_rules()
        else:
            messages.error(request, 'Error saving form')
        
    form = Symptoms()
    form2 = Diagnosis()
    form3 = System_rules()
    return render(request, 'kb_temps/kb_interface.html', context = {
     "symptoms_form":form,
     "diagnosis_form":form2,
     "system_rules":form3,
        })
       