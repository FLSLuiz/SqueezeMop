from django.contrib.auth import views
from django.urls import path
from core.views import index, shop, signup, account, edit_account
from product.views import product

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('account/', account, name='account'),
    path('account/edit/', edit_account, name='edit_account'),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>/', product, name='product'), 
]
