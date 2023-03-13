from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	user_type = forms.ChoiceField(choices=(
        ('normal', 'Normal User'),
        ('expert', 'Expert'),
    ))

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(
        ('normal', 'Normal User'),
        ('expert', 'Expert'),
    ))

#class ForgotPasForm(forms.Form):
#	email = forms.EmailField(required=True)

#class d_Questions(forms.Form):
