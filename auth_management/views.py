from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse

def home(request):
    return render(request, 'gallery/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('auth_management:home')
        else:
            messages.error(request, '사용자명 또는 비밀번호가 잘못되었습니다.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('auth_management:home')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}님의 계정이 생성되었습니다!')
            return redirect('auth_management:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
