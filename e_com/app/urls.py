from django .urls import path 
from . import views


urlpatterns = [
    path('',views.e_com_login),
    path('shop_home',views.shop_home),
    path('logout',views.e_com_logout),
    path('add product',views.e_com_addpro),
    
]
