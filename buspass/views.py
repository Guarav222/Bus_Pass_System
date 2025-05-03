
import random

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from datetime import datetime, timedelta, time
from datetime import date



# Create your views here.

def index(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'index.html', locals())

def pass_Enquiry(request):
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
    try:
        pas = Pass.objects.filter(PassNumber=sd)
    except:
        pas = ""
    return render(request, 'pass_Enquiry.html', locals())

def view_PassEnquiryDtls(request,pid):
    pas = Pass.objects.get(id=pid)
    return render(request, 'view_PassEnquiryDtls.html', locals())



def admin_home(request):
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    lasts = today - timedelta(7)

    tpass = Pass.objects.filter(PasscreationDate=today).count()
    ypass = Pass.objects.filter(PasscreationDate=yesterday).count()
    lspass = Pass.objects.filter(PasscreationDate__gte=lasts, PasscreationDate__lte=today).count()
    totalpass = Pass.objects.all().count()
    cat = Category.objects.all().count()
    unread = Contact.objects.filter(isread="no").count()
    read = Contact.objects.filter(isread="yes").count()

    return render(request, 'admin_home.html', locals())


def add_Category(request):
    error = ""
    if request.method == "POST":
        catname = request.POST['categoryname']
        try:
            Category.objects.create(categoryname=catname)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Category.html', locals())


def manage_Category(request):
    cat = Category.objects.all()
    return render(request, 'manage_Category.html', locals())


def edit_Category(request, pid):
    cat = Category.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        catname = request.POST['categoryname']

        cat.categoryname = catname

        try:
            cat.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_Category.html', locals())


def delete_Category(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('manage_Category')


def add_Pass(request):
    error = ""
    category1 = Category.objects.all()
    if request.method == "POST":
        pn = str(random.randint(10000000, 99999999))
        fn = request.POST['FullName']
        pimg = request.FILES['ProfileImage']
        cno = request.POST['ContactNumber']
        email = request.POST['Email']
        itype = request.POST['IdentityType']
        icardno = request.POST['IdentityCardno']
        ct = request.POST['category']
        source = request.POST['Source']
        dest = request.POST['Destination']
        fdate = request.POST['FromDate']
        todate = request.POST['ToDate']
        cost = request.POST['Cost']

        category = Category.objects.get(id=ct)

        try:
            Pass.objects.create(PassNumber=pn, FullName=fn, ProfileImage=pimg, ContactNumber=cno, Email=email,
                                IdentityType=itype, IdentityCardno=icardno, category=category, Source=source,
                                Destination=dest,
                                FromDate=fdate, ToDate=todate, Cost=cost, PasscreationDate=date.today())
            error = "no"
        except:
            error = "yes"


    return render(request, 'add_Pass.html', locals())


def manage_Pass(request):
    pas = Pass.objects.all()
    return render(request, 'manage_Pass.html', locals())


def edit_Pass(request, pid):
    pas = Pass.objects.get(id=pid)
    category1 = Category.objects.all()
    error = ""
    if request.method == "POST":
        fn = request.POST['FullName']
        cno = request.POST['ContactNumber']
        email = request.POST['Email']
        itype = request.POST['IdentityType']
        icardno = request.POST['IdentityCardno']
        ct = request.POST['category']
        source = request.POST['Source']
        dest = request.POST['Destination']
        fdate = request.POST['FromDate']
        todate = request.POST['ToDate']
        cost = request.POST['Cost']

        category = Category.objects.get(id=ct)

        pas.FullName = fn
        pas.ContactNumber = cno
        pas.Email = email
        pas.IdentityType = itype
        pas.IdentityCardno = icardno
        pas.category = category
        pas.Source = source
        pas.Destination = dest
        pas.Cost = cost

        if fdate:
            pas.FromDate = fdate
        if todate:
            pas.ToDate = todate

        try:
            pas.save()
            error = "no"
        except:
            error = "yes"

        try:
            pimg = request.FILES['ProfileImage']
            pas.ProfileImage = pimg
            pas.save()
        except:
            pass
    return render(request, 'edit_Pass.html', locals())


def view_PassDetails(request, pid):
    pas = Pass.objects.get(id=pid)
    return render(request, 'view_PassDetails.html', locals())


def delete_Pass(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    pas = Pass.objects.get(id=pid)
    pas.delete()
    return redirect('manage_Pass')


def search(request):
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
    try:
        pas = Pass.objects.filter(Q(PassNumber=sd) | Q(ContactNumber=sd))
    except:
        pas = ""
    return render(request, 'search.html', locals())


def betweendate_report(request):
    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']
        pas = Pass.objects.filter(Q(PasscreationDate__gte=fd) & Q(PasscreationDate__lte=td))
        return render(request, 'bookingbtwdates.html', locals())
    return render(request, 'betweendate_report.html')


def changePassword(request):
    error = ""
    if request.method == "POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    return render(request, 'changePassword.html', locals())

def Logout(request):
    logout(request)
    return redirect('index')

def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['emailid']
        c = request.POST['contact']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n, emailid=e, contact=c, message=m, msgdate=date.today(), isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

def delete_contact(request,pid):
    contact = Contact.objects.get(id=pid)
    contact.delete()
    return redirect('read_queries')

