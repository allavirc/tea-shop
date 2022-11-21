from django.contrib import admin
from django.urls import (
    path,
    include
)
from shop import settings
from django.conf.urls.static import static
from server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('user/', include('auths.urls')),

    path('', views.home, name='home'),
    path('', include('server.urls')),
    path('search/', views.Search.as_view(), name='post_list_url'),

    # path('', include('django.contrib.auth.urls')),
    path('catalog/', views.products, name='catalog'),
    path('blacktea/catalog/', views.products, name='catalog'),
    path('greentea/catalog/', views.products, name='catalog'),
    path('redtea/catalog/', views.products, name='catalog'),
    path('whitetea/catalog/', views.products, name='catalog'),
    path('reletedtea/catalog/', views.products, name='catalog'),
    path('puertea/catalog/', views.products, name='catalog'),

    path('add_to_basket/', views.add_to_basket, name="add_to_basket"),
    path('logout/', views.logout_view, name='logout'),
    path('sing-up/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('basket/', views.BasketView.as_view(), name="basket"),
    path('add_product/', views.BasketView.as_view(), name="add_product"),
    path('main/', views.LoginView.as_view(), name='main'),


    # Catalog (tea)
    path('products/', views.products),
    path('productss/', views.ProductList.as_view()),
    path('blacktea/', views.blacktea),
    path('greentea/', views.greentea),
    path('redtea/', views.redtea),
    path('puertea/', views.puertea),
    path('whitetea/', views.whitetea),
    path('reletedtea/', views.reletedtea),

    path('Black tea/', views.blacktea),
    path('Green tea/', views.greentea),
    path('Red tea/', views.redtea),
    path('Puer tea/', views.puertea),
    path('White tea/', views.whitetea),
    path('Releted tea/', views.reletedtea)
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

