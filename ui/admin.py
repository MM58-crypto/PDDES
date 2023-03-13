from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Question, Choice

# Register your models here.


# group selected questions
@admin.action(description='Group selected questions')
def group_questions(Question, request, queryset):
    # action to group questions (using a queryset method)
    # group the questions inside the model and add a title for each group
    selected_questions = {}
    print('.....')
    Question.message_user(request, ngettext(
        '%d The selected questions were grouped successfully', 
        updated,
    ) % updated, messages.SUCCESS)


class Choice_Inline(admin.TabularInline):
    model = Choice
    extra = 1

class Question_Admin(admin.ModelAdmin):
    fieldsets = [
         (None,          {'fields':[ 'question_text', ]}),
    ]
    inlines = [Choice_Inline]
    actions=[group_questions]




admin.site.register(Question,  Question_Admin )