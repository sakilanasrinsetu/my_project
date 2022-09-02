from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=250)
    icon = models.ImageField(upload_to = 'category',
     null= True, blank = True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
         null=True, blank=True, related_name='products'
    )
    image = models.ImageField(upload_to = 'product',
     null= True, blank = True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

