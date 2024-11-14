from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import product
# Create your views here.

def e_com_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        shop=authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            req.session['shop']=uname       #create
            return redirect(shop_home)
        else:
            messages.warning(req,'invalid username or password')
            return redirect(e_com_login)
    else:
        return render(req,'login.html')
    

def e_com_logout(req):
    logout(req)
    req.session.flush()        #delete
    return redirect(e_com_login)

def e_com_addpro(req):
    return render(req,'shop/add.html')

def shop_home(req):
    if 'shop' in req.session:
        products=product.objects.all()
        return render(req,'shop/home.html',{'products':products})
    else:
        return redirect(e_com_login)


def add(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            dis=req.POST['dis']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            stock=req.POST['stock']
            img=req.FILES['img']
            data=product.objects.create(pid=pid,name=name,dis=dis,price=price,offer_price=offer_price,stock=stock,img=img)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/add.html')  
    else:
        return redirect(e_com_login)    



def edit_product(req,id):
    if req.method=='POST':
        pid=req.POST['pid']
        name=req.POST['name']
        dis=req.POST['dis']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        img=req.FILES.get('img')
        if img:
            product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis,price=price,offer_price=offer_price,stock=stock)
            data=product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
             product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis,price=price,offer_price=offer_price,stock=stock)
        return redirect(shop_home)     
    else:
        data=product.objects.get(pk=id)        
        return render(req,'shop/edit.html',{'data':data})
                
                
                
#------------------------------------------------user-------------------------------------------------------              
            
        