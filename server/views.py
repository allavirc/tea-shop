from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse,
    HttpRequest, JsonResponse,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DetailView

from auths.models import CustomUser
from cart.forms import CartAddProductForm
from server.models import Product, Comment, Basket, BasketItem
from server.forms import ProductForm, RegistrationForm, AddProductToBasketForm
from django.contrib import messages
from django.db.models import Q


def product_list(request, category_slug=None):
    category = None
    categories = Product.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Product, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'server/catalog.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'cart/detail.html', {'product': product,
                                                       'cart_product_form': cart_product_form})









class Search(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        all_products = Product.objects.all()
        search_products = []
        for item in all_products:
            if request.POST.get('search').lower() in item.title.lower():
                search_products.append(item)
        return render(
            request=request,
            template_name="server/search.html",
            context={"search": search_products}
        )



class ProductList(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False)


class ProductDetail(DetailView):
    model = Product
    pk_url_kwarg = "id"


def home(request):
    return render(request, 'server/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user: CustomUser = CustomUser()
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.set_password(form.cleaned_data.get('password'))
            user.set_password(form.cleaned_data.get('password_confirm'))
            user.save()
            Basket.objects.create(client=user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegistrationForm()
    return render(request,
                  'server/sing-up.html',
                  {'form': form})


class AddProductView(LoginRequiredMixin, FormView):
    template_name = "server/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog")

    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required(login_url=reverse_lazy("login"))
def add_to_basket(request):
    user = request.user
    basket = user.basket
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    try:
        my_product = BasketItem.objects.get(product=product)
        my_product.quantity += 1
        my_product.save()

    except:
        BasketItem.objects.create(
                basket=basket,
                product=product,
            )

    return JsonResponse(data={
            "count": basket.items.count()
        }), render(
        template_name='server/basket.html',
        context={
            "count": basket.items.count()
        }
    )

# @login_required(login_url=reverse_lazy("login"))
# def add_to_basket(request):
#     try:
#         user = request.user
#         basket = user.basket
#         product_id = request.POST.get("product_id")
#         product = get_object_or_404(Product, id=product_id)
#         try:
#             my_product = BasketItem.objects.get(product=product)
#             my_product.quantity += 1
#             my_product.save()
#             return JsonResponse(data={
#                 "count": basket.items.count()
#             })
#         except:
#             BasketItem.objects.create(
#                 basket=basket,
#                 product=product,
#             )
#
#             return JsonResponse(data={
#                 "count": basket.items.count()
#             })
#     except:
#         return render(
#             request,
#             template_name="server/add_product.html",
#             context={
#                 'basket': basket
#             }
#         )


# Создаём вьюшку для обработки запросы на "Корзина"
class BasketView(View):

    # Наш гет запрос
    #
    def get(self, request, *args, **kwargs):
        # Берём пользователя из запроса от html страницы
        user: CustomUser = request.user

        # Достём из базы данных корзину АВТОРИЗИРОВАННОГО пользователя (client=user)
        try:
            basket: Basket = Basket.objects.get(client=user)
        except Basket.DoesNotExist:
            basket = None


        # Проверим, нашёл ли он корзину
        if not basket:
            return render(
                request=request,
                template_name="server/basket.html",
                context={"basket_items": ["YOU ARE NOT HAVE BASKET"]}
            )

        # Берём все продукты из КОРЗИНЫ ПОЛЬЗОВАТЕЛЯ из базы данных
        basket_items = BasketItem.objects.filter(basket=basket)
        context = {"basket_items": basket_items}
        return render(
            request=request,
            template_name="server/basket.html",
            context=context
        )

    def post(self, request, *args, **kwargs):
        pass


def main_view(request):
    return render(request, template_name='server/main.html', context={})


# /logout
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse("main"))
    return HttpResponse("Вы не залогинены")

#
#
# class RegisterView(FormView):
#     template_name = 'server/login.html'
#     form_class = RegistrationForm
#     success_url = reverse_lazy("main")
#
#     def form_valid(self, form):
#         CustomUserManager.objects.create_user(**form.cleaned_data)
#         return super().form_valid(form)
#
#
class LoginView(FormView):
    template_name = "server/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("main")


    def form_valid(self, form):
        user = authenticate(
            request=self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user:
            login(self.request, user)
            return redirect(reverse("main"))
        else:
            return render(
                request=self.request,
                template_name='server/login.html',
                context={
                    'form': form,
                    'error': "Не верное имя пользователя или пароль"
                }
            )
        return super().form_valid(form)



# def autoris_user(request):
#     image = Product.objects.get(id=2).image
#     if request.method == 'GET':
#         form = AutorisUserForm()
#         return render(
#             request=request,
#             template_name='server/autorisUser.html',
#             context={'form': form}
#         )
#
#     return render(
#         request=request,
#         template_name='server/autorisUser.html',
#         context={
#             'a': 'Вы авторизированы!',
#             'image': image,
#         }
#     )


class AddProduct(FormView):
    template_name = "server/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# def form_data(request):
#     if request.method == 'GET':
#         form = RegistrationForm()
#
#         return render(
#             request, 'server/form_data.html',
#             context={
#                 'form': form,
#             },
#         )
#     else:
#         form = RegistrationForm(request.POST)
#         if form.is_valid:
#             return render(
#                 request, 'server/form_data.html',
#                 context={
#                     'form': form,
#                 },
#             )
#
#         else:
#             return render(
#                 request, 'server/form_data.html',
#                 context={
#                     'form': form,
#                 },
#             )

def productid(request, id):
    product = Product.objects.get(id=id)
    return render(
        request,
        'server/productid.html',
        context={
            'product': product,

        }
    )

def products(request):
    product1 = Product.objects.get(id=3)
    product2 = Product.objects.get(id=4)
    product3 = Product.objects.get(id=5)
    product4 = Product.objects.get(id=6)
    product5 = Product.objects.get(id=7)
    product6 = Product.objects.get(id=8)

    return render(
        request,
        'server/catalog.html',
        context={
            'product1': product1,
            'product2': product2,
            'product3': product3,
            'product4': product4,
            'product5': product5,
            'product6': product6,

        }
    )

def blacktea(request):
    product1 = Product.objects.get(id=3)

    return render(
        request,
        'server/tea/blacktea.html',
        context={
            'product1': product1

        }
    )


def greentea(request):
    product2 = Product.objects.get(id=4)

    return render(
        request,
        'server/tea/greentea.html',
        context={
            'product2': product2

        }
    )

def redtea(request):
    product3 = Product.objects.get(id=5)

    return render(
        request,
        'server/tea/redtea.html',
        context={
            'product3': product3

        }
    )

def puertea(request):
    product4 = Product.objects.get(id=6)

    return render(
        request,
        'server/tea/puertea.html',
        context={
            'product4': product4

        }
    )

def whitetea(request):
    product5 = Product.objects.get(id=7)

    return render(
        request,
        'server/tea/whitetea.html',
        context={
            'product5': product5

        }
    )

def reletedtea(request):
    product6 = Product.objects.get(id=8)

    return render(
        request,
        'server/tea/reletedtea.html',
        context={
            'product6': product6

        }
    )


