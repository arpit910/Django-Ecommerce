from django.shortcuts import redirect, render
from .models import *
from django.db.models.query import QuerySet

# Create your views here.
def home(request):
    return render(request,'home.html',{'posts':Post.objects.all()})

def gallery(request):
    return render(request,'gallery.html',{'gallery':Gallery.objects.all()})    

def product(request):
    if request.user.is_authenticated:
        productwl=Profile.objects.get(user=request.user).product_wishlist.all()
    else:
        productwl=[]
    if "shop" in request.path_info:
        products=Products.objects.filter(isCctv=False)
    elif "cctv" in request.path_info:
        products=Products.objects.filter(isCctv=True)
    return render(request,'products.html',{'products':products,'wl':productwl})    

def about(request):
    return render(request,'about.html',{'members':Members.objects.all(),'Stats':Stats.objects.all(),'cr':customer_review.objects.all()})    

def showproduct(request,name):
    Product=Products.objects.get(name=name)
    if request.user.is_authenticated:
        productwl=Profile.objects.get(user=request.user).product_wishlist.all()
    else:
        productwl=[]
    return render(request,'showproduct.html',{'product':Product,'wl':productwl})    

def profile(request):
    if request.user.is_authenticated:
        pwl=Profile.objects.get(user=request.user).product_wishlist.all()
        return render (request,"profile.html",{"wishlist":pwl})
    else:
        return redirect('signin')

def add2wl(request,id,parent):
    product=Products.objects.get(id=id)
    if request.method=="POST":
        profile=Profile.objects.get(user=request.user)
        if product in profile.product_wishlist.all():
           profile.product_wishlist.remove(product)
        else:
            profile.product_wishlist.add(product)
        if parent=='shop':
            return redirect('/shop')
        elif parent=='cctv':
            return redirect('/cctv')
        elif parent=='product':
            return redirect("/showproduct/"+product.name)
    else:
        return redirect("/showproduct/"+product.name)
                