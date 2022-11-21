from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db.models import QuerySet, Q, CASCADE
from django.db.models.functions import Length
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)



class Product(models.Model):
    title = models.CharField("Название", max_length=255)
    price = models.IntegerField("Цена")
    description = models.TextField("Описание", default="")
    image = models.ImageField("Фотография", null=True, upload_to='products')
    image2 = models.ImageField("Фотография", null=True, upload_to='products')
    image3 = models.ImageField("Фотография", null=True, upload_to='products')
    reiting = models.FloatField("Рейтинг", default=0)

    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        return 1

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'



class CustomUserManager(BaseUserManager):

    def create_user(self, password, first_name, last_name, email, date_of_birth, number, is_active, is_staff, data_joined) ->'CustomUser':
        if not email:
            raise ValidationError('Email required')
        if not first_name:
            raise ValidationError('First name required')
        if not last_name:
            raise ValidationError('Last name required')
        if not number:
            raise ValidationError('Number required')
        if not is_active:
            raise ValidationError('Is active required')
        if not is_staff:
            raise ValidationError('Is staff required')
        if not data_joined:
            raise ValidationError('Date joined required')

        user: 'CustomUser' = self.model(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=self.normalize_email(email),
            number=number,
            is_active=is_active,
            is_staff=is_staff,
            data_joined=data_joined
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email) -> 'CustomUser':
        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            password=password,
            email=self.normalize_email(email),
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.hobbies = Hobbies.objects.first()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_info(self):
        print('Custom user Manager!!!')

    def get_special_user(self) -> QuerySet:
        """Get users where is_staff = True, and join gte 01.07.2022."""
        users: QuerySet[CustomUser] = self.filter(
            Q(is_staff=True) &
            Q(data_joined__gte=datetime.date(2022, 7, 1))
        )
        return users

    def get_active_user(self):
        """Get users where is_active = True"""
        users = self.filter(
            is_active=True
        )
        return users

    def get_many_hobbies(self):
        """Get user if he has many then 3 hobbies"""
        queryset = CustomUser.objects.annotate(hob_len=Length('Hobbies')).filter(hob_len__gt=3)
        return queryset


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USERS_HOBBIES = [
        ('F', 'Football'),
        ('D', 'Drawing'),
        ('d', 'Dancing'),
        ('B', 'Baseball'),
        ('R', 'Running')
    ]

    email = models.EmailField(
        'Почта/Логин', unique=True
    )
    number = models.CharField(
        'Номер телефона', max_length=11,
    )
    is_active = models.BooleanField(
        'Активность', default=True
    )
    is_staff = models.BooleanField(
        'Статус менеджера', default=False
    )
    data_joined = models.DateTimeField(
        'Время создания', default=timezone.now
    )

    hobbies = models.CharField(
        max_length=1,
        null=True,
        choices=USERS_HOBBIES,
        default='d'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = (
            'data_joined',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Hobbies(models.Model):
    name = models.CharField(
        'Название',
        max_length=255,
        unique=True
    )







