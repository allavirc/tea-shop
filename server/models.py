from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from auths.models import CustomUser


class Product(models.Model):
    title = models.CharField("Название", max_length=255)
    price = models.IntegerField("Цена")
    description = models.TextField("Описание", default="")
    image = models.ImageField("Фотография", null=True, upload_to='products')
    image2 = models.ImageField("Фотография", null=True, upload_to='products')
    image3 = models.ImageField("Фотография", null=True, upload_to='products')
    reiting = models.FloatField("Рейтинг", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

class Comment(models.Model):
    author = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)



class Basket(models.Model):
    client = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class BasketItem(models.Model):
    basket = models.ForeignKey(
        Basket, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

