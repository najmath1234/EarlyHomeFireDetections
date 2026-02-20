from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import Alerts, Users, Complaints


def login_get(request):
    return render(request,'login.html')
def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    check=authenticate(request,username=username,password=password)
    if check is not None:
        login(request,check)
        if check.groups.filter(name='admin').exists():
            return redirect('/myapp/adminhome_get/')
        elif check.groups.filter(name='user').exists():
            return redirect('/myapp//')
        else:
            return redirect('/myapp/login_get/')
    else:
        return redirect('/myapp/login_get/')


def forgetpasswword_get(request):
    return render(request,'forgetpassword.html')
def forgetpassword_post(request):
    return

def logout_get(request):
    logout(request)


#A D M I N--------------------------------------------

def adminhome_get(request):
    return render(request,'admins/adminhome.html')

def changepassword_get(request):
    return render(request,'admins/changepassword.html')
def changepassword_post(request):
    currentpassword=request.POST['currentpassword']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['confirmpassword']
    data=request.user
    if data.check_password(currentpassword):
        if newpassword==confirmpassword:
            data.set_password(newpassword)
            data.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/changepassword_get/')
    else:
        return redirect('/myapp/changepassword_get/')


def sentreply_get(request,id):
    return render(request,'admins/sentreply.html',{'id':id})
def sentreply_post(request):
    reply=request.POST['Reply']
    id=request.POST['id']
    a =  Complaints.objects.get(id=id)
    a.reply=reply
    a.status='replyed'
    a.save()
    return redirect('/myapp/viewcomplaint_get/')


def viewalerts_get(request):
    a=Alerts.objects.all()
    return render(request,'admins/viewalerts.html',{'alert':a})

def viewblockedusers_get(request):
    a=Users.objects.all()
    return render(request,'admins/viewblockeduser.html',{'blocked':a})

def viewcomplaint_get(request):
    a =  Complaints.objects.all()
    return render(request,'admins/viewcomplaint.html',{'complaint':a})

def viewuser_get(request):
    a = Users.objects.filter(status='pending')
    return render(request,'admins/viewuser.html',{'users':a})


def block_user(request,id):
    Users.objects.filter(id=id).update(status='blocked')
    return redirect('/myapp/viewuser_get/')


#U S E R----------------------------------------------
def editprofile_get(request):
    return render(request,'users/editprofile.html')
def editprofile_post(request):
    return


def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')
def sentcomplaint_post(request):
    return

def signup_get(request):
    return render(request,'users/signup.html')
def signup_post(request):
    return

def viewprofile_get(request):
    return render(request,'users/viewprofile.html')

def viewreply_get(request):
    return render(request,'users/viewreply.html')

def ratingandreview_get(request):
    return render(request,'users/ratingandreview.html')
def ratingandreviw_post(request):
    return
