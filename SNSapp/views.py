from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import SnsModel,AppUsers,Follow,Coment
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
    context = {}
    context_list = []
    print(request.user)
    user = User.objects.filter(username=request.user).first()
    print(user.id)
    #カレントユーザー
    appuser = AppUsers.objects.filter(user=user).first()
    print(appuser)
    sns_list = SnsModel.objects.all().order_by('-id')

    for sns_row in sns_list:
        sns_dict = {}
        sns_dict["sns_obj"] = sns_row
        sns_dict["current_user"] = appuser
        sns_dict["comment_count"] = len(sns_row.coment_set.all())
        sns_dict["comment_list"] = sns_row.comment_set.all()
        follow_check = Follow.objects.filter(user=appuser,user_2=sns_row.user).first()
        if follow_check:
            follow_check = True
        else:
            follow_check = False
        sns_dict["follow_check"] = follow_check
        context_list.append(sns_dict)
    context["sns_context"] = context_list
    print(context)
    return render(request, 'list.html', context)

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
    user_posts = appuser.snsmodel_set.all()
    friend_list = appuser.follow_user.filter(user=appuser.id)
    followed_friend_list = appuser.followed_user.filter(user_2=appuser.id)
    context = {
        "appuser":appuser, 
        "user_posts": user_posts, 
        "friend_list": friend_list,
        "posts_count": len(user_posts),
        "friend_count": len(friend_list),
        "followed_friend_list": followed_friend_list,
        "followed_count": len(followed_friend_list)
    }    

    return render(request, 'mypage.html', context)

def mypageUpdatefunc(request, pk):
    if request.method == "GET":
        appuser = AppUsers.objects.filter(pk=pk).first()
        user_posts = appuser.snsmodel_set.all()
        friend_list = appuser.follow_user.filter(user=appuser.id)
        followed_friend_list = appuser.followed_user.filter(user_2=appuser.id)
        context = {
            "appuser":appuser, 
            "user_posts": user_posts, 
            "friend_list": friend_list,
            "posts_count": len(user_posts),
            "friend_count": len(friend_list),
            "followed_friend_list": followed_friend_list,
            "followed_count": len(followed_friend_list)

        }
        return render(request, 'mypageupdate.html', context)
    
    if request.method == "POST":
        appuser = AppUsers.objects.filter(pk=pk).first()
        if request.FILES:
            appuser.images = request.FILES['images']
        else:
            appuser.name = request.POST['name']
            appuser.age = request.POST['age']
            appuser.company = request.POST['company']
            appuser.hoby = request.POST['hoby']
            appuser.birthplace = request.POST['birthplace']
            appuser.introduction = request.POST['introduction']
        appuser.save()
        return redirect('mypage', pk=appuser.user.pk)

def snsCreate(request):
    if request.method == "GET":
        return render(request, 'create.html')
    if request.method == "POST":
        print(request.POST)
        print(request.FILES['images'])
        sns = SnsModel()
        sns.title = request.POST["title"]
        sns.content = request.POST["content"]
        sns.images = request.FILES["images"]
        sns.author = request.POST["author"]
        user_id = request.POST["user"]
        appuser = AppUsers.objects.filter(user=user_id).first()
        sns.user = appuser
        sns.save()
        return redirect('list')

def followfunc(request, user_id, followed_user_id):   
    appuser_id = AppUsers.objects.filter(user=user_id).first()
    appuser2_id = AppUsers.objects.filter(id=followed_user_id).first()
    follow_object = Follow.objects.filter(user=appuser_id,user_2=appuser2_id).first()
    followed_object = Follow.objects.filter(user=appuser2_id,user_2=appuser_id).first()
    print(user_id,followed_user_id)
    #すでに対象ユーザーをフォローしている場合はリダイレクト
    if follow_object:
        return redirect('list')
    #対象ユーザーからフォローされていればフォローを承認処理
    elif followed_object:
        if followed_object.shonin_status == 0:
            followed_object.shonin_status = 1
            followed_object.save()
        else:
            #すでに承認済み
            return redirect('list')
    else:
        follow_object = Follow()
        follow_object.user = appuser_id
        follow_object.user_2 = appuser2_id
        follow_object.save()
        return redirect('list')

def commentfunc(request):
    test = request
    data = request.POST
    comment_content = data.get('comment', None)
    current_user_id = data.get('current_user_id', None)
    sns_user_id = data.get('sns_user_id', None)
    sns_id = data.get('sns_id', None)
    
    if comment_content:
        comment = Coment()
        comment.comment = comment_content
        comment.comment_user_id = int(current_user_id)
        comment.user_id = int(sns_user_id)
        comment.sns_id = int(sns_id)
        comment.save()

    print(request)




class SnsCreate(CreateView):
    template_name = 'create.html'
    model = SnsModel
    fields = ('title','content','images','author','user')
    success_url = reverse_lazy('list')


