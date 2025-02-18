from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout


def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
