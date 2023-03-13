from django import forms
from ui.models import Question, Choice
from inference_engine.models import GHQ12Question, GHQ12Response


class QuestionForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[18:23]: # 18:23
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = {}
        for field_name, field_value in self.cleaned_data.items():
            selected_choices[field_name] = field_value
        return selected_choices

        # anxiety [6:11] 
        # sa [0:5]
        # depression [31:37]
        # anti-social [23:30]
        # ptsd [12:18]
        # ocd [18:23]
        # bipolar [37:46]
        #gen_qs [47:58]
        # use an if statement to direct user to group of specific questions
        # based on answer of general questions 
#class Gen_Questions_Form(forms.Form):
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        score = 0
#        gen_questions = Question.objects.all()[47:58]
#        for question in gen_questions: 
#            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
#            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

class GHQ12Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in GHQ12Question.objects.all():
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.question_text,
                choices=((0, 'Better than usual'), (1, 'No more than usual'), (2, 'Rather more than usual'), (3, 'Much more than usual')),
                widget=forms.RadioSelect
            )

    def save(self):
        responses = []
        for field_name, response in self.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = field_name.split('_')[-1]
                question = GHQ12Question.objects.get(id=question_id)
                responses.append(GHQ12Response(question=question, response=response))
        GHQ12Response.objects.bulk_create(responses)