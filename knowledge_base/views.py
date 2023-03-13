from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Psych_D_symptoms, Disorder_Diagnosis
from .forms import Symptoms, Diagnosis, System_rules
# Create your views here.


# change the kb-interface so that expert can select a disorder and
# info of that disorder is displayed
# use foreign key to link  
@login_required(login_url='/accounts/login/')
def disorder_info_view(request):
    if request.method == "POST":

        form = Symptoms(request.POST)
        form2 = Diagnosis(request.POST)
        #form3 = System_rules(request.POST)
        if form.is_valid():
            kb_data = form.save()
            messages.success(request, "Data added to the Knowledge base Successfully")
            form = Symptoms()
        
        if form2.is_valid():
            kb_data = form2.save()
            dropdown_value = form2.cleaned_data['disorder_name'] # get the selected value from the form
            disorder_data = Disorder_Diagnosis.objects.get(disorder_name=dropdown_value)
            messages.success(request, "Data added to the Knowledge base Successfully")
            form2 = Diagnosis(instance=disorder_data)

        #if form3.is_valid():
        #    kb_data = form3.save()
        #    messages.success(request, "Data added to the Knowledge base Successfully")
        #    form3 = System_rules()
        else:
            messages.error(request, 'Error saving form')
        
    
    form = Symptoms()
    form2 = Diagnosis()
    #form3 = System_rules()
    #fetch data from db & render to the kb interface
    #disorders_data = Disorder_Diagnosis.objects.filter(user=request.user)
    #symptoms_data = Psych_D_symptoms.objects.filter(user=request.user)
    context = {
     "symptoms_form": form,
     "diagnosis_form": form2,
     #"system_rules":form3,
        }
    return render(request, 'kb_temps/kb_interface.html', context)

# view function to retrieve the data from the database
def get_data(request):
    id = request.GET.get(id=id)
    symptoms_data = Psych_D_symptoms.objects.get(id=id)
    return JsonResponse({'symptom_name': symptoms_data.symptom_name,
     'symptom_desc': symptoms_data.symptom_desc,
        })
       