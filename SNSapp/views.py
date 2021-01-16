from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import SnsModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

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
            return render(request, 'login.html', {'some':100})
    return render(request, 'signup.html', {'some':100})

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            print("no user")
            return redirect('login')
    return render(request, 'login.html')

@login_required
def listfunc(request):
    object_list = SnsModel.objects.all()
    return render(request, 'list.html', {"object_list": object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request, pk):
    object = SnsModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object': object})

def goodfunc(request, pk):
    post = SnsModel.objects.get(pk=pk)
    post.good = post.good + 1
    post.save()
    return redirect('list')

def readfunction(request, pk):
    post = SnsModel.objects.get(pk=pk)
    read_check = request.user.get_username()
    if read_check in post.readtext:
        return redirect('list')
    else:
        post.read = post.read +1
        post.readtext = post.readtext + ' ' + read_check
        post.save()
        return redirect('list')

class SnsCreate(CreateView):
    template_name = 'create.html'
    model = SnsModel
    fields = ('title','content','images','author')
    success_url = reverse_lazy('list')


