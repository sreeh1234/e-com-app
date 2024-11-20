from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

# Create your views here.

def e_com_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        shop=authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            if shop.is_superuser:
                
                req.session['shop']=uname       #create
                return redirect(shop_home)
            else:
                req.session['user']=uname
                return redirect(user_home)
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
    
    
def delete(req,pid):
    data=product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)
                
                
                
#------------------------------------------------user-------------------------------------------------------              
            
def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']        
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
            return redirect(e_com_login)
        except:
            messages.warning(req,'Email Already Exist')
            return redirect(register)
    else:
        return render(req,'user/register.html')    
    
def user_home(req):
    if 'user' in req.session:
        products=product.objects.all()
        return render(req,'user/home.html',{'products':products})
    else:
        return redirect(e_com_login)
    
def view_product(req,pid):
    data=product.objects.get(pk=pid) 
    return render(req,'user/view.html',{'data':data})   

def add_to_cart(req,pid):
    products=product.objects.get(pk=pid) 
    user=User.objects.get(username=req.session['user'])
    try:
        Cart=cart.objects.get(product=products,user=user)
        Cart.qty+=1
        Cart.save()
    except:    
        data=cart.objects.create(product=products,user=user,qty=1)
        data.save()
    return redirect(view_cart)


def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})


def qty_incri(req,cid):
    data=cart.objects.get(pk=cid)
    print(data.qty)
    print(data.product.stock)
    if data.product.stock > data.qty:
        data.qty+=1
        data.save()
    return redirect(view_cart)   


def qty_dec(req,cid):
    data=cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    if data.qty==0:
        data.delete()
    return redirect(view_cart)  

def buy_product(req,pid):
    products=product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=products.offer_price
    buy=Buy.objects.create(product=products,user=user,qty=qty,t_price=price)
    return redirect(user_bookings)

def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    bookings=Buy.objects.filter(user=user)
    return render(req,'user/bookings.html',{'bookings':bookings})