from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import math

from .models import User


def index(request):
    return render(request, "Cal/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Cal/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Cal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Cal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Cal/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Cal/register.html")

def trigo(request):
    return render(request, "Cal/trigo.html")

def logln(request):
    return render(request, "Cal/logln.html")
        
def strigo(request):
    if request.method == "POST":
        fn = request.POST["fn"]
        x = float(request.POST["x"])
        unit = request.POST["unit"]
        if unit != "radian":
            x = x * math.pi/180
        res = 0
        if fn == "sin":
            res = math.sin(x)
        elif fn == "cos":
            res = math.cos(x)
        elif fn == "tan":
            res = math.tan(x)
        elif fn == "cosec":
            try:
                res = 1/math.sin(x)
            except:
                res = float('inf')
        elif fn == "sec":
            try:
                res = 1/math.cos(x)
            except:
                res = float('inf')
        elif fn == "cot":
            try:
                res = 1/math.tan(x)
            except:
                res = float('inf')
        
        if res >= 100000000000:
            res = float('inf')
        elif res <= -1000000000:
            res = float('inf')

        return render(request, "Cal/trigo.html", {
            "res" : round(res, 2)
        })

def slogln(request):
    if request.method == "POST":
        fn = request.POST["fn"]
        x = float(request.POST["x"])
        res = 0
        error = ""
        eorn = False
        if x<=0:
            error = "Value must be +ve"
            eorn = True
            return render(request, "Cal/logln.html", {
            "error" : error,
            "eorn" : eorn,
        })
        if fn == "log":
            base = float(request.POST["base"])
            if (base <= 0 or base==1):
                error = "Base must be +ve and not 1"
                eorn = True
                return render(request, "Cal/logln.html", {
                "error" : error,
                "eorn" : eorn,
            })
            res = math.log(x, base)
        else:
            res = math.log(x)
        return render(request, "Cal/logln.html", {
            "res" : res,
            "eorn" : eorn,
        })

def hcflcm(request):
    return render(request, "Cal/hcflcm.html")


def gcd(a, b):
    if (a == 0):
        return b
    return gcd(b % a, a)
 
def lcm(arr, idx):
    if (idx == len(arr)-1):
        return arr[idx]
    a = arr[idx]
    b = lcm(arr, idx+1)
    return int(a*b/gcd(a,b))

def shcflcm(request):
    if request.method == "POST":
        fn = request.POST["fn"]
        res = 0 
        eorn = False
        error = ""
        x = request.POST["x"]
        y = (x.split(","))
        for z in y:
            if z == "0":
                error = "All numbers must be positive"
                eorn = True
                return render(request, 'Cal/hcflcm.html', {
                    'error': error,
                    'eorn': eorn
                    })  
        if fn == "lcm":
            nl = []
            for i in range(len(y)):
                n = int(y[i])
                nl.append(n)
            res = lcm(nl,0)
        else:
            n1= int(y[0])
            n2= int(y[1])
            hcf=gcd(n1,n2)
            
            for i in range(2,len(y)):
                hcf=gcd(hcf,int(y[i]))
            res = hcf
        return render(request, 'Cal/hcflcm.html', {
            'res': res,
            'eorn': eorn
            })
            
def qe(request):
    return render(request, 'Cal/qe.html')

def sqe(request):
    if request.method == 'POST':
        a = int(request.POST["a"])
        error = ""
        eorn = False
        b = int(request.POST["b"])
        c = int(request.POST["c"])
        x1 = 0
        x2 = 0
        e1 = False
        e2 = False
        eb = False

        if (a <= 0):
            error = "a cannot be 0"
            eorn = True
            return render(request, 'Cal/qe.html', {
                "eorn": eorn,
                "error": error,
            })

        try:
            x1 = (-b+math.sqrt(b**2-4*a*c))/2*a
        except:
            e1 = True

        try:
            x2 = (-b-math.sqrt(b**2-4*a*c))/2*a
        except:
            e2 = True

        if (e1 and e2):
            eb = True
            e1 = False
            e2 = False
        return render(request, 'Cal/qe.html', {
            "x1": round(x1,3),
            "x2": round(x2,3),
            "e1": e1,
            "e2": e2,
            "eb": eb,
            "eorn": eorn
        })

def stats(request):
    return render(request, 'Cal/stats.html')

def sstats(request):
    if request.method == 'POST':
        x = request.POST["x"]
        y = (x.split(","))
        nl = []
        for i in range(len(y)):
            n = int(y[i])
            nl.append(n)
        nl.sort()
        m = 0
        for n in nl:
            m = m + n/len(nl)
        M = 0
        l = int(len(nl)/2)
        if len(nl)%2 == 0:
            M = (nl[l-1]+ nl[l])/2
        else:
            M = (nl[l])/2
        md = 0
        Md = 0
        vari = 0
        sd = 0
        for n in nl:
            md = md + abs(n-m)/len(nl)
            Md = Md + abs(n-M)/len(nl)
            vari = vari + (n-m)**2/len(nl)
        sd = math.sqrt(vari)
        r = max(nl) - min(nl)
        cv = m/sd*100

        return render(request, "Cal/stats.html", {
            "mean": m,
            "M": M,
            "meand": md,
            "Md": Md,
            "var": vari,
            "sd": round(sd, 3),
            "range": r,
            "cv": round(cv,3)
        })
        