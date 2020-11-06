from django.contrib import admin
from django.urls import path
from userpage import views
from userpage.views import Search_User, Post_Detail,AddCommentView, Profile_Detail


urlpatterns = [
    path('', views.userHome, name='userhome'),
    path('post', views.userPost, name='post'),
    path("profile/<int:pk>", Profile_Detail.as_view(), name='profiles'),
    path("deletepost/<str:Uid>", views.delPost, name='deletepost'),
    path('Like', views.userLike, name='likepost'),
    path("user/follow/<str:username>", views.follow, name="follow"),
    path("search/", Search_User.as_view(), name="search"),
    path("post_detail/<int:pk>", Post_Detail.as_view(), name="post_detail"),
    path("like/<int:pk>", views.LikeView,name="like_post"),
    path('post_detail/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),




]
