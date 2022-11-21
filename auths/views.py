from django.contrib.auth import authenticate, login, logout
from django.http import (
    HttpResponse,
    HttpRequest,
)
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse
from django.views.generic import ListView

from auths.forms import RegistrationForm, ProductForm, RegisterUserForm, AutorisUserForm, LoginForm
from auths.models import CustomUser


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(
            request=request,
            template_name='server/login.html',
            context={'form': form}
        )

    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(
            request=request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user:
            login(request, user)
            return redirect(reverse("main"))
        else:
            render(
                request=request,
                template_name='server/login.html',
                context={
                    'form': form,
                    'error': "Не верное имя пользователя или пароль"
                }
            )

    return render(
        request=request,
        template_name='server/login.html',
        context={'form': form}
    )

def hello(request):
    return request

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse("main"))
    return HttpResponse("Вы не залогинены")


def register_user(request):
    if request.method == 'GET':
        form = RegisterUserForm()
        return render(
            request=request,
            template_name='server/registerUser.html',
            context={'form': form}
        )
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        user: CustomUser = CustomUser()
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        return render(
            request=request,
            template_name='server/registerUser.html',
            context={'a': 'Вы успешно зарегистрировались!'
            }
        )

    return render(
        request=request,
        template_name='server/registerUser.html',
        context={'form': form,
                 }
    )

def autoris(request):
    form = AutorisUserForm()

    return render(
        request,
        'server/autorisUser.html',
        context={
            'form': form,
            'a': None

        }
    )

def register(request):
    form = RegistrationForm()

    return render(
        request,
        'server/registerUser.html',
        context={
            'form': form,
            'a': None
        }
    )

def autoris_user(request):
    if request.method == 'GET':
        form = AutorisUserForm()
        return render(
            request=request,
            template_name='server/autorisUser.html',
            context={'form': form}
        )

    return render(
        request=request,
        template_name='server/autorisUser.html',
        context={
            'a': 'Вы авторизированы!',
        }
    )
