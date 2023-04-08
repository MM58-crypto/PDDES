from django.contrib import admin
from .models import  GHQ12Question, GHChoice
# Register your models here.



class GHQ_Choice_Inline(admin.TabularInline):
    model = GHChoice
    extra = 1

class GHQ_Question_Admin(admin.ModelAdmin):
    fieldsets = [
         (None,          {'fields':[ 'question_text', ]}),
    ]
    inlines = [GHQ_Choice_Inline]
    



admin.site.register(GHQ12Question, GHQ_Question_Admin)
#admin.site.register(GHQ12Response)