from django.contrib import admin
from .models import Psych_D_symptoms, Disorder_Diagnosis, System_rules
# Register your models here.

admin.site.register(Psych_D_symptoms)
admin.site.register(Disorder_Diagnosis)
admin.site.register(System_rules)
