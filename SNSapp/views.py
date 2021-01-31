from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import SnsModel,AppUsers,Follow
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            if not username or not password:
                return render(request, 'signup.html', {'error':'ユーザー名とパスワードを入れてください'})
            User.objects.get(username=username)
            return render(request, 'signup.html', {'error':'このユーザーは登録されています。'})
        except:
            user = User.objects.create_user(username, '', password)
            appuser = AppUsers(password=password,name=username,user=user)
            appuser.save()
            return redirect('login')
    return render(request, 'signup.html')

def loginfunc(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST['username']
        user_check = User.objects.filter(username=username)
        password = request.POST['password']
        #認証チェック
        if not user_check:
            return render(request,'login.html', {"error": "ユーザーネームが間違っています"})
        user = authenticate(request, username=username, password=password)
        #アプリ内で扱うユーザー作成
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            print("no user")
            return render(request, 'login.html', {"error":"パスワードが間違っています。"})

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

def mypagefunc(request, pk):
    print("#######")
    print(request.user.get_username)
    appuser = AppUsers.objects.filter(user=pk).first()
    return render(request, 'mypage.html', {"appuser":appuser})

def mypageUpdatefunc(request, pk):
    if request.method == "GET":
        appuser = AppUsers.objects.filter(pk=pk).first()
        return render(request, 'mypageupdate.html', {"appuser":appuser})
    if request.method == "POST":
        print(request.POST['name'])
        appuser = AppUsers.objects.filter(pk=pk).first()
        appuser.name = request.POST['name']
        appuser.age = request.POST['age']
        appuser.company = request.POST['company']
        appuser.hoby = request.POST['hoby']
        appuser.birthplace = request.POST['birthplace']
        appuser.introduction = request.POST['introduction']
        appuser.save()
        return redirect('mypage', pk=appuser.user.pk)


class SnsCreate(CreateView):
    template_name = 'create.html'
    model = SnsModel
    fields = ('title','content','images','author')
    success_url = reverse_lazy('list')


