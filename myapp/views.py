import subprocess
from datetime import datetime

import sys
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

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
            u=Users.objects.get(AUTHUSER=check.id)
            if u.status == "pending":
                return redirect('/myapp/userhome_get/')
            else:
                messages.error(request, 'Account blocked')
                return redirect('/myapp/login_get/')
        else:
            messages.error(request, 'Invalid User')
            return redirect('/myapp/login_get/')
    else:
        messages.error(request, 'Invalid User')
        return redirect('/myapp/login_get/')




def forgot_get(request):
    # return render(request,"loginpage.html")
    return render(request,"forgot.html")
def forgot_post(request):
    email=request.POST['username']
    l=User.objects.filter(username=email)
    if l.exists():
        p = User.objects.get(username=email)
        import random
        psw=str(random.randint(0000,9999))
        send_mail("temp password", psw, settings.EMAIL_HOST_USER, [email])
        p.set_password(psw)
        p.save()
        return redirect("/myapp/loginpage_get/")
    else:
        messages.error(request, 'Invalid Email')
        return redirect("/myapp/forgot_get/")


def logout_get(request):
    logout(request)
    return redirect("/myapp/login_get/")


#A D M I N--------------------------------------------
@login_required(login_url="/myapp/login_get/")
def adminhome_get(request):
    return render(request,'admins/adminhome.html')

@login_required(login_url="/myapp/login_get/")
def changepassword_get(request):
    return render(request,'admins/changepassword.html')

@login_required(login_url="/myapp/login_get/")
def changepassword_post(request):
    currentpassword=request.POST['currentpassword']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['confirmpassword']
    data=request.user
    if data.check_password(currentpassword):
        if newpassword==confirmpassword:
            data.set_password(newpassword)
            data.save()
            messages.success(request, 'Password Changed Successfully')
            return redirect('/myapp/login_get/')
        else:
            messages.error(request, 'Current password not match')
            return redirect('/myapp/changepassword_get/')
    else:
        messages.error(request, 'New password and Confirm Password dont match')
        return redirect('/myapp/changepassword_get/#a')

@login_required(login_url="/myapp/login_get/")
def sentreply_get(request,id):
    return render(request,'admins/sentreply.html',{'id':id})

@login_required(login_url="/myapp/login_get/")
def sentreply_post(request):
    reply=request.POST['Reply']
    id=request.POST['id']
    a = Complaints.objects.get(id=id)
    a.reply=reply
    a.status='replied'
    a.save()
    messages.success(request, 'Replied Successfully')
    return redirect('/myapp/viewcomplaint_get/#a')

@login_required(login_url="/myapp/login_get/")
def viewalerts_get(request):
    a=Alerts.objects.all().order_by("-id")
    return render(request,'admins/viewalerts.html',{'alert':a})

@login_required(login_url="/myapp/login_get/")
def viewblockedusers_get(request):
    a=Users.objects.filter(status='blocked')
    return render(request,'admins/viewblockeduser.html',{'blocked':a})

@login_required(login_url="/myapp/login_get/")
def viewcomplaint_get(request):
    a = Complaints.objects.all()
    return render(request,'admins/viewcomplaint.html',{'complaint':a})

@login_required(login_url="/myapp/login_get/")
def viewuser_get(request):
    a = Users.objects.filter(status='pending')
    return render(request,'admins/viewuser.html',{'users':a})

@login_required(login_url="/myapp/login_get/")
def block_user(request,id):
    Users.objects.filter(id=id).update(status='blocked')
    return redirect('/myapp/viewuser_get/#a')

@login_required(login_url="/myapp/login_get/")
def unblock_user(request,id):
    Users.objects.filter(id=id).update(status='pending')
    return redirect('/myapp/viewuser_get/#a')

@login_required(login_url="/myapp/login_get/")
def deletealertuser(request,id):
    Alerts.objects.get(id=id).delete()
    return redirect('/myapp/userviewalerts_get/#a')


@login_required(login_url="/myapp/login_get/")
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

        if User.objects.filter(username=email).exists():
            messages.success(request, 'Email Already Exists')
            return redirect("/myapp/register_get/")

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

@login_required(login_url="/myapp/login_get/")
def userhome_get(request):
    return render(request,'users/userhome.html')

@login_required(login_url="/myapp/login_get/")
def editprofile_get(request):
    data=Users.objects.get(AUTHUSER=request.user)
    return render(request,'users/editprofile.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
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

    if User.objects.filter(username=email).exclude(id=request.user.id).exists():
        messages.error(request, 'Email Already Exists')
        return redirect("/myapp/editprofile_get/#a")
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
    messages.success(request, 'Updated Successfully')
    return redirect("/myapp/viewprofile_get/#a")

@login_required(login_url="/myapp/login_get/")
def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')

@login_required(login_url="/myapp/login_get/")
def sentcomplaint_post(request):
    complaint = request.POST['complaint']

    data=Complaints()
    data.complaint=complaint
    data.date=datetime.now().date()
    data.reply='pending'
    data.status='pending'
    data.USER=Users.objects.get(AUTHUSER=request.user)
    data.save()
    messages.success(request, 'Sended Successfully')
    return redirect("/myapp/viewreply_get/#a")


def signup_get(request):
    return render(request,'users/signup.html')
def signup_post(request):
    return

@login_required(login_url="/myapp/login_get/")
def viewprofile_get(request):
    data=Users.objects.get(AUTHUSER=request.user)
    return render(request,'users/viewprofile.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def viewreply_get(request):
    data=Complaints.objects.filter(USER__AUTHUSER=request.user)
    return render(request,'users/viewreply.html',{'reply':data})

@login_required(login_url="/myapp/login_get/")
def ratingandreview_get(request):
    return render(request,'users/ratingandreview.html')

@login_required(login_url="/myapp/login_get/")
def ratingandreviw_post(request):
    review=request.POST['review']
    rating=request.POST['rating']

    d=Reviews()
    d.review=review
    d.rating=rating
    d.date = datetime.now().date()
    d.USER = Users.objects.get(AUTHUSER=request.user)
    d.save()
    messages.success(request, 'Sended Successfully')
    return redirect("/myapp/userhome_get/#a")

@login_required(login_url="/myapp/login_get/")
def user_changepassword_get(request):
    return render(request,'users/userchangepassword.html')

@login_required(login_url="/myapp/login_get/")
def user_changepassword_post(request):
    currentpassword=request.POST['currentpassword']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['confirmpassword']
    data=request.user
    if data.check_password(currentpassword):
        if newpassword==confirmpassword:
            data.set_password(newpassword)
            data.save()
            messages.success(request, 'Password Changed Successfully')
            return redirect('/myapp/login_get/')
        else:
            messages.error(request, 'Current password not match')
            return redirect('/myapp/user_changepassword_get/#a')
    else:
        messages.success(request, 'New password and Confirm Password dont match')
        return redirect('/myapp/user_changepassword_get/#a')

@login_required(login_url="/myapp/login_get/")
def userviewalerts_get(request):
    a=Alerts.objects.filter(USER__AUTHUSER=request.user).order_by("-id")
    return render(request,'users/viewalerts.html',{'alert':a})


@csrf_exempt
def upload_detection(request):
    label = request.POST['label']
    image = request.POST['image']
    lid = request.POST['lid']


    obj=Alerts()
    obj.time=datetime.now().time()
    obj.date=datetime.now().date()
    obj.label=label
    obj.image=image
    obj.USER=Users.objects.get(AUTHUSER=lid)
    obj.save()

    return JsonResponse({'status': 'success', 'message': 'Detection saved'})

@login_required(login_url="/myapp/login_get/")
def predict(request):
    process = subprocess.Popen(
        [sys.executable, "C:\\Users\\najum\\PycharmProjects\\yoloearlyhomefiredetection\\myapp\\prediction.py", str(request.user.id), str("f")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # with open(PID_FILE, "w") as f:
    #     f.write(str(process.pid))
    return redirect('/myapp/userhome_get/')