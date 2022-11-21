from django import forms
from django.core.exceptions import ValidationError
from auths.models import Product, CustomUser


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'image', 'image2', 'image3', 'reiting']


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        data = self.cleaned_data
        if len(data.get('password')) < 8:
            raise ValidationError(
                'Слишком легкий пароль!'
            )

        else:
            return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email):
            raise ValidationError(
                'Пользователь с таким email уже существует!'
            )

        else:
            return email



class RegisterUserForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")


    def clean_username(self):
        cleaned_data = super().clean()
        if len(CustomUser.objects.filter(email=cleaned_data.get('email'))) > 0:
            raise ValidationError(
                "Пользователь уже есть!"
            )
        return self.cleaned_data.get('email')

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password"
        ]


class AutorisUserForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if len(CustomUser.objects.filter(username=cleaned_data.get('username')) and
               CustomUser.objects.filter(password=cleaned_data.get('password'))) > 0:
            raise Exception(
                "Логин или пароль не верен!"
            )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password"
        ]

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)