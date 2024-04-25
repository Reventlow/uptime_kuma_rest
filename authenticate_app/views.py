from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ("Forkert brugernavn og/eller adgangskode"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.error(request, ("Du er logget ud"))
    return redirect('authenticate_app:login')


@login_required(login_url='login')
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Bruger er blevet registreret"))
            return redirect('authenticate_app:home')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'register_user.html', context)


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("Din bruger info er opdateret"))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'edit_profile.html', context)


@login_required(login_url='authenticate_app:login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("Din adgangskode er opdateret"))
            return redirect(':authenticate_app:home')
    else:
        form = ChangePasswordForm(user=request.user)
    context = {'form': form}
    return render(request, 'change_password.html', context)
