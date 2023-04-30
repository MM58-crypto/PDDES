from django import forms
from ui.models import Question, Choice
from inference_engine.models import GHQ12Question, GHChoice


 #question groups :- 
        # anxiety [6:11] 
        # sa [0:5]
        # depression [28:35]
        # ptsd [11:17]
        # ocd [17:22]
        # anti-social [22:28]
        # bipolar 
        # based on answer of general questions 
        # use an if statement to direct user to group of specific questions

class Social_Anxiety(forms.Form): # currently for all qs 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[0:5]: 
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = Question.objects.get(id=int(field_name))
            selected_choice = Choice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices

class Anxiety_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[5:11]: 
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = Question.objects.get(id=int(field_name))
            selected_choice = Choice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices

class Depression_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[28:35]: 
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = Question.objects.get(id=int(field_name))
            selected_choice = Choice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices

class bipolar_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[35:42]: 
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = Question.objects.get(id=int(field_name))
            selected_choice = Choice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices

class Antisocial_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[22:28]: 
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = Question.objects.get(id=int(field_name))
            selected_choice = Choice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices

class ptsd_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[11:17]: 
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = Question.objects.get(id=int(field_name))
            selected_choice = Choice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices

class ocd_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in Question.objects.all()[17:22]: 
            choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = Question.objects.get(id=int(field_name))
            selected_choice = Choice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices
       
      

class GHQ12Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for question in GHQ12Question.objects.all():
            choices = [(choice.id, choice.choice_text) for choice in question.ghchoice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label=question.question_text)

    def get_selected_choices(self):
        selected_choices = []
        # change from field_value to choice text
        for field_name, field_value in self.cleaned_data.items():
            question = GHQ12Question.objects.get(id=int(field_name))
            selected_choice = GHChoice.objects.get(id=int(field_value))
            selected_choices.append((question.question_text, selected_choice.choice_text))
        return selected_choices
  