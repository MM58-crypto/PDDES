"""my_pddes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views

from ui import views 

from knowledge_base.views import *
from inference_engine.views import *
from django.urls import path, include 



urlpatterns = [
    path('', views.home_view, name="homepage"), 
    path('about/', views.about_view), 
    path('register/', views.register_request, name="register"),
    path('help/', views.help_view), 
    path('contact/', views.contact_view), 
    path('admin/', admin.site.urls),
    path('test/',  d_test_view, name="test"),
    path('ghq/', ghq_view, name="ghq"),
    path('anxiety_test/', anxiety_page_view),
    path('sa_anxiety_test/', socialanxiety_page_view),
    path('depression_test/', depression_page_view),
    path('ocd_test/', ocd_view),
    path('antisocial_test/', antisocial_view),
    path('ptsd_test/', ptsd_page_view),
    #bipolar is left 
    


    path('results/', results_view, name="results"),   
    path('accounts/login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('expert_ui/', views.expert_ui_view, name="expert_ui"),
    path('normal_dash/', views.normal_dashboard_view,name="normal_dash"), 
    

    
    path('password_reset/', views.password_reset_view, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password-related/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password-related/confirm_password.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password-related/complete_pw_reset.html'), name='password_reset_complete'),      
    #path("accounts/", include("django.contrib.auth.urls")),
    # kb stuff
    path("kb-interface/<int:id>", disorder_info_view, name="kb-interface"),
    path('get_disorder_info/', get_disorder_info, name='get_disorder_info'),
]
