from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('hello/', views.hello_world),
    # path('info/', views.all_right),
    # path('square/<int:number>', views.square),
    # path('power/<int:number>/<int:power>', views.power),
    # path('calc/<int:number><str:znack><int:power>', views.calc),
    # path('html/', views.html),
    # path('helloname/<str:name>', views.hello_name),
    # path('powerh/<int:number>/<int:power>', views.html_power),
    # path('squares/<int:n>', views.for_squares),
    path('products/', views.products),
    path('products/<int:id>', views.products),
    path('products/server/blacktea.html', views.blacktea),

    path('', views.home, name='home'),
    path('home', views.home, name='home'),
]