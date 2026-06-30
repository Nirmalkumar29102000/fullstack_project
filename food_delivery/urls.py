"""
URL configuration for food_delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base, name='base'),
    path('register/',register, name='register'),
    path('login',login,name='login'),
    path('customer_dashboard', customer_dashboard,name='customer_dashboard'),
    path('owner_dashboard', owner_dashboard,name='owner_dashboard'),
    path('delivery_dashboard', delivery_dashboard,name='delivery_dashboard'),
    path('add_restaurant', add_restaurant,name='add_restaurant'),
    path('view_restaurant',view_restaurant,name='view_restaurant'),
    path('add_food/<int:restaurant_id>/',add_food, name='add_food'),
    path('view_food/<int:restaurant_id>/',view_food,name='view_food'),
    path('edit_food/<int:id>/',edit_food,name='edit_food'),
    path('delete_food/<int:id>/',views.delete_food,name='delete_food'),
    path('view_menu/<int:restaurant_id>/',views.view_menu,name='view_menu'),
    path('add_to_cart/<int:food_id>/',views.add_to_cart,name='add_to_cart'),
    path('view_cart/',views.view_cart,name='view_cart'),
    path('place_order/',views.place_order,name='place_order'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('owner_orders/',views.owner_orders,name='owner_orders'),
    path('accept_order/<int:id>/',views.accept_order,name='accept_order'),
    path('deliver_order/<int:id>/',views.deliver_order,name='deliver_order'),
    path('payment_page/',views.payment_page,name='payment_page'),
    path('logout/', views.logout, name='logout')
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )