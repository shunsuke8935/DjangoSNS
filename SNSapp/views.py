from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        save_check = User.objects.filter(username=username).first()
        if save_check:
            return render(request, 'signup.html', {'error':'このユーザーは登録されています。'})
        else:
            user = User.objects.create_user(username, '', password)
            print(request.POST)
            return render(request, 'signup.html', {'some':100})
    return render(request, 'signup.html', {'some':100})

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('signup')
        else:
            print("no user")
            return redirect('login')
    return render(request, 'login.html')

def listfunc(request):
    return render(request, 'list.html')
