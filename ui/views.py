from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users

def home_view(request):

    return render(request, "gen_webpages/index-new.html")

def about_view(request):
    return render(request, "gen_webpages/about.html")

def help_view(request):
    return render(request, "gen_webpages/help.html")

def contact_view(request):
    # make contact form work 
    if request.method == "POST":
        #do smth
        print('temp line')
    return render(request, "gen_webpages/contact.html")

@login_required(login_url='/accounts/login/')

@allowed_users(allowed_roles=['experts', 'admin'])
def expert_ui_view(request):
    # additional code to be added later
    
    return render(request, "dashboards/expert_ui.html")

@login_required(login_url='/accounts/login/')
def normal_dashboard_view(request):
    # additional code to maybe added later

    return render(request, "dashboards/normal_dash.html")


# reconfigure to send email to an actual email address
# current function sends email to terminal 

def password_reset_view(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password-related/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.success(request, "An email has been sent to your email address with password reset instructions")
                    #return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password-related/Password_reset.html", context={"password_reset_form":password_reset_form})
 

@unauthenticated_user
def login_view(request):
   if request.method=="POST":
        form = LoginForm(request.POST)
        #form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            user = authenticate(request, username=username, password=password)
            
           # messages.success(request, "Successfully Logged in!")
           # issue: normal user can login and view expert dashboard and viceversa 
            if user is not None:
                if user_type == 'normal':
                    login(request,user)
                    messages.info(request, f"Welcome, {username}")
                    # redirects normal user to their dashboard
                    return redirect('normal_dash')
                elif user_type == 'expert':
                    login(request,user)
                    messages.info(request, f"Welcome, {username}")
                    # redirects expert user to experts dashboard 
                    return redirect('expert_ui')
            else:
                messages.error(request, "Invalid credentials/error, try again!")
        else:
            messages.error(request, "Invalid credentials/error, try again!")
   form = LoginForm()
   return render(request, 'registration/login.html', context = {'login_form': form}) 

def logout_view(request):
    logout(request)
    messages.info(request, "Successfully logged out.")
    return redirect("homepage")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("homepage")
        messages.error(request, "Registration unsuccessful. invalid info")
    form = NewUserForm()
    return render (request=request, template_name="registration/signup.html", context={"register_form":form})



