from django.urls import path
from .views import signupfunc, loginfunc, listfunc, logoutfunc, detailfunc, goodfunc, readfunction, snsCreate, mypagefunc, mypageUpdatefunc,followfunc

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('list/', listfunc, name='list'),
    path('logout/', logoutfunc, name='logout'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('follow/<int:user_id>/<int:followed_user_id>', followfunc, name='followfunc'),
    path('read/<int:pk>', readfunction, name='read'),
    path('create/', snsCreate, name='create'),
    path('mypage/<int:pk>', mypagefunc, name='mypage'),
    path('mypageupdate/<int:pk>', mypageUpdatefunc, name='mypageupdate')
]
