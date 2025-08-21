from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm
from store.forms import RegistrationForm
from carts.models import Order

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'extending/login.html', {'error': 'Invalid credentials'})
    return render(request, 'extending/login.html')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'extending/register.html', {'form': form})

@login_required
def dashboard(request):
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'extending/dashboard.html', {"recent_orders": recent_orders})


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'extending/profile.html', {"form": form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'extending/change_password.html', {"form": form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'extending/orders.html', {"orders": orders})
