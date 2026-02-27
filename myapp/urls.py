"""
URL configuration for yoloearlyhomefiredetection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views
#A D M I N---------------------------------------------------
urlpatterns = [
   path('login_get/',views.login_get),
   path('login_post/',views.login_post),
   path('logout_get/', views.logout_get),

   path('forgetpasswword_get/',views.forgetpasswword_get),
   path('forgetpassword_post/',views.forgetpassword_post),

   path('changepassword_get/',views.changepassword_get),
   path('changepassword_post/',views.changepassword_post),

   path('sentreply_get/<id>',views.sentreply_get),
   path('sentreply_post/',views.sentreply_post),

   path('viewalerts_get/',views.viewalerts_get),

   path('viewblockedusers_get/',views.viewblockedusers_get),

   path('viewcomplaint_get/',views.viewcomplaint_get),

   path('viewuser_get/',views.viewuser_get),

   path('adminhome_get/',views.adminhome_get),

   path('block_user/<id>',views.block_user),

   path('viewrating/',views.viewrating_get),





#U S E R-------------------------------------------------------
   path('register_get/',views.register_get),
   path('register_post/',views.register_post),

   path('userhome_get/',views.userhome_get),

   path('editprofile_get/',views.editprofile_get),
   path('editprofile_post/',views.editprofile_post),

   path('sentcomplaint_get/',views.sentcomplaint_get),
   path('sentcomplaint_post/',views.sentcomplaint_post),

   path('signup_get/',views.signup_get),
   path('signup_post/',views.signup_post),

   path('viewprofile_get/',views.viewprofile_get),

   path('viewreply_get/',views.viewreply_get),

   path('ratingandreview_get/',views.ratingandreview_get),
   path('ratingandreviw_post/',views.ratingandreviw_post),



   path('user_changepassword_get/',views.user_changepassword_get),
   path('user_changepassword_post/',views.user_changepassword_post),

]
