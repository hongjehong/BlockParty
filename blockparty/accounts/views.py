from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods, require_POST
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('blocks:index')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            auth_login(request, get_user(request))
            return redirect('blocks:index')
        
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('blocks:index')
    if request.method == "POST":
        auth_form = AuthenticationForm(request, request.POST)
        if auth_form.is_valid():
            auth_login(request, auth_form.get_user())
            return redirect(request.GET.get('next') or 'blocks:index')

    else:
        auth_form = AuthenticationForm()
    context = {
        'auth_form': auth_form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('blocks:index')

def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blocks:index')

    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form':form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('blocks:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password.html', context)