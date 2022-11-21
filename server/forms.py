from django import forms

from auths.models import CustomUser
from server.models import Product, BasketItem


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    date_of_birth = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=DateInput
    )
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        data = self.cleaned_data
        if len(data.get('password')) < 8:
            raise forms.ValidationError(
                'Слишком легкий пароль!'
            )

        if data['password'] != data['password_confirm']:
            raise forms.ValidationError('Пароли не совпадают!')


        else:
            return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email):
            raise forms.ValidationError(
                'Пользователь с таким email уже существует!'
            )

        else:
            return email


    def clean_date_of_birth(self):
        data = self.cleaned_data
        date_of_birth = self.cleaned_data.get('date_of_birth')
        age = 14
        if age < 14:
            raise forms.ValidationError(
                'Сайт доступен пользователям от 14+'
            )

        else:
            return data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'image', 'image2', 'image3', 'reiting']


# class RegisterUserForm(forms.ModelForm):
#     repeat_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Сюда пароль второй раз!',
#             'class': 'rep'
#             }),
#         label="Повторите пароль"
#     )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         repeat_password = cleaned_data.pop("repeat_password")
#         if password != repeat_password:
#             raise forms.ValidationError(
#                 "Пароли не совпадают"
#             )
#         return cleaned_data
#
#     def clean_username(self):
#         cleaned_data = super().clean()
#         if len(CustomUser.objects.filter(email=cleaned_data.get('email'))) > 0:
#             raise forms.ValidationError(
#                 "Пользователь уже есть!"
#             )
#         return self.cleaned_data.get('email')
#
#     class Meta:
#         model = CustomUser
#         fields = [
#             # "username",
#             # "first_name",
#             # "last_name",
#             "email",
#             "password"
#         ]
#
#
class AutorisUserForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")


        if len(CustomUser.objects.filter(email=cleaned_data.get('email')) and CustomUser.objects.filter(password=password)) < 0:
            raise Exception(
                "Логин или пароль не верен!"
            )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password"
        ]


class AddProductToBasketForm(forms.ModelForm):
    class Meta:
        model = BasketItem
        exclude = ["id"]

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=255)
#     password = forms.CharField(max_length=255)

