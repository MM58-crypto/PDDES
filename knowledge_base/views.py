from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from knowledge_base.models import Psych_D_symptoms, Disorder_Diagnosis
from .forms import Symptoms, Diagnosis
# Create your views here.


# change the kb-interface so that expert can select a disorder and
# info of that disorder is displayed
# use foreign key to link  
@login_required(login_url='/accounts/login/')

def disorder_info_view(request, id):
    disorder_obj = get_object_or_404(Disorder_Diagnosis, id=id)

    if request.method == 'POST':
        form = Diagnosis(request.POST, instance=disorder_obj)
        if form.is_valid():
            form.save()
            # maybe change message to Disorder modified successfully 
            messages.success(request, "Knowledge Base modified successfully")
    else:
        form = Diagnosis(instance=disorder_obj)

    disorders = Disorder_Diagnosis.objects.all()
    context = {
        'diagnosis_form': form,
        'disorders': disorders,
    }

    return render(request, 'kb_temps/kb_interface.html', context)

def get_disorder_info(request):
    disorder_id = request.GET.get('disorder_id')
    disorder = Disorder_Diagnosis.objects.get(pk=disorder_id)
    data = {
        'disorder_desc': disorder.disorder_desc,
        'disorder_keywords': disorder.disorder_keywords,
        'recommendation': disorder.recommendation,
    }
    return JsonResponse(data)