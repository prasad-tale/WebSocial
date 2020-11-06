from django.contrib import admin
from django.urls import path
from account import views
from django.contrib import admin


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('login', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),

]
