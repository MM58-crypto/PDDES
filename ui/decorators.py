from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

# this func takes the login view func as an argument 
# easier way and faster to determine if user is authenticated or not
# prevents user from accessing login page if already logged in
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You are not authoized to view or access expert ui page. You have been redirected to your dashboard")
                return redirect('/normal_dash')
                #return HttpResponse("You are not authoized to view or access this page")
        return wrapper_func
    return decorator