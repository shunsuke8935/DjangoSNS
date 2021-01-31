from django.urls import path
from .views import signupfunc, loginfunc, listfunc, logoutfunc, detailfunc, goodfunc, readfunction, SnsCreate, mypagefunc, mypageUpdatefunc

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('list/', listfunc, name='list'),
    path('logout/', logoutfunc, name='logout'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('read/<int:pk>', readfunction, name='read'),
    path('create/', SnsCreate.as_view(), name='create'),
    path('mypage/<int:pk>', mypagefunc, name='mypage'),
    path('mypageupdate/<int:pk>', mypageUpdatefunc, name='mypageupdate')
]
