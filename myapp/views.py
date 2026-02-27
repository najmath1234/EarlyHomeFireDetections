from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import Alerts, Users, Complaints, Reviews


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
            return redirect('/myapp/userhome_get/')
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
    return redirect("/myapp/login_get/")


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
    a = Complaints.objects.get(id=id)
    a.reply=reply
    a.status='replyed'
    a.save()
    return redirect('/myapp/viewcomplaint_get/')


def viewalerts_get(request):
    a=Alerts.objects.all()
    return render(request,'admins/viewalerts.html',{'alert':a})

def viewblockedusers_get(request):
    a=Users.objects.filter(status='blocked')
    return render(request,'admins/viewblockeduser.html',{'blocked':a})

def viewcomplaint_get(request):
    a = Complaints.objects.all()
    return render(request,'admins/viewcomplaint.html',{'complaint':a})

def viewuser_get(request):
    a = Users.objects.filter(status='pending')
    return render(request,'admins/viewuser.html',{'users':a})


def block_user(request,id):
    Users.objects.filter(id=id).update(status='blocked')
    return redirect('/myapp/viewuser_get/')

def viewrating_get(request):
    a=Reviews.objects.all()
    return render(request,'admins/viewrating.html',{'data':a})


#U S E R----------------------------------------------
def register_get(request):
    return render(request,'users/Register.html')
def register_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    phone=request.POST['phone']
    email=request.POST['email']
    place=request.POST['place']
    city=request.POST['city']
    district=request.POST['district']
    pincode=request.POST['pincode']
    photo=request.FILES['photo']
    password=request.POST['password']
    conpassword=request.POST['confirmpassword']

    if password==conpassword:

        fs=FileSystemStorage()
        date=datetime.now().strftime('%d%M%Y%H%M%S')+'.jpg'
        fs.save(date,photo)
        file_name=fs.url(date)

        a=User.objects.create_user(username=email,password=conpassword)
        a.groups.add(Group.objects.get(name='user'))
        a.save()

        u=Users()
        u.name=name
        u.dob=dob
        u.email=email
        u.phone=phone
        u.gender=gender
        u.place=place
        u.city=city
        u.district=district
        u.pincode=pincode
        u.photo=file_name
        u.status='pending'
        u.AUTHUSER=a
        u.save()

        messages.success(request,'Registered successfully')
        return redirect("/myapp/login_get/")
    else:
        messages.error(request, 'Password does not match')
        return redirect("/myapp/register_get/")


def userhome_get(request):
    return render(request,'users/userhome.html')

def editprofile_get(request):
    return render(request,'users/editprofile.html')
def editprofile_post(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    phone = request.POST['phone']
    email = request.POST['email']
    place = request.POST['place']
    city = request.POST['city']
    district = request.POST['district']
    pincode = request.POST['pincode']

    u=Users.objects.get(AUTHUSER=request.user)
    t=u.AUTHUSER
    t.username=email
    t.save()


    if 'photo' in request.FILES:

        photo=request.FILES["photo"]
        fs = FileSystemStorage()
        date = datetime.now().strftime('%d%M%Y%H%M%S') + '.jpg'
        fs.save(date, photo)
        file_name = fs.url(date)
        u.photo=file_name
        u.save()
    u.name = name
    u.dob = dob
    u.email = email
    u.phone = phone
    u.gender = gender
    u.place = place
    u.city = city
    u.district = district
    u.pincode = pincode
    u.save()

    return redirect("/myapp/viewprofile_get/")


def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')
def sentcomplaint_post(request):
    complaint = request.POST['complaint']

    data=Complaints()
    data.complaint=complaint
    data.date=datetime.now().date()
    data.reply='pending'
    data.status='pending'
    data.USER=Users.objects.get(AUTHUSER=request.user)
    data.save()
    return redirect("/myapp/viewreply_get/")


def signup_get(request):
    return render(request,'users/signup.html')
def signup_post(request):
    return

def viewprofile_get(request):
    data=Users.objects.get(AUTHUSER=request.user)
    return render(request,'users/viewprofile.html',{'data':data})

def viewreply_get(request):
    data=Complaints.objects.filter(USER__AUTHUSER=request.user)
    return render(request,'users/viewreply.html',{'reply':data})

def ratingandreview_get(request):
    return render(request,'users/ratingandreview.html')
def ratingandreviw_post(request):
    review=request.POST['review']
    rating=request.POST['rating']

    d=Reviews()
    d.review=review
    d.rating=rating
    d.date = datetime.now().date()
    d.USER = Users.objects.get(AUTHUSER=request.user)
    d.save()
    return redirect("/myapp/userhome_get/")

def user_changepassword_get(request):
    return render(request,'admins/changepassword.html')
def user_changepassword_post(request):
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
            return redirect('/myapp/user_changepassword_get/')
    else:
        return redirect('/myapp/user_changepassword_get/')

