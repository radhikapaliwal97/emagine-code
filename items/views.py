from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Item
from django.contrib import messages


@login_required(login_url="/login/")
def HomePage(request):
    items = Item.objects.filter(user=request.user)
    return render(request, 'home.html', {'items': items})

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')        
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if not uname or not pass1 or not pass2:
            messages.error(request, "All fields must be filled out.")
            return redirect('signup')
        
        if pass1!=pass2:
            messages.error(request,"Your password and confirm password are not Same!!")
        if User.objects.filter(username=uname).exists():
            messages.error(request,"Username already exists. Please choose a different one.")
            return redirect('signup')
        
        my_user = User.objects.create_user(uname, password=pass1)
        my_user.save()

        return redirect('login') 
    
    return render(request, 'signup.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        if not username or not pass1:
            messages.error(request, "All fields must be filled out.")
            return redirect('login')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is incorrect!!!")
            return redirect('login')

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
 

@login_required(login_url="/login/")
def add_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_price = request.POST.get('price')
        
        if item_name and item_price:
            Item.objects.create(name=item_name, price=item_price, user=request.user)        
    return redirect('home')

@login_required(login_url="/login/")
def summary(request):    
    items = Item.objects.filter(user=request.user)
    total_cost = int(sum(item.price for item in items))
    return render(request, 'summary.html',{'total_cost': total_cost})