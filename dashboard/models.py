from django.db import models
from django.contrib.auth.models import User


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



class UserProfile(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	address = models.CharField(max_length=100, null=True, blank=True)
	town = models.CharField(max_length=100, null=True, blank=True)
	county = models.CharField(max_length=100, null=True, blank=True)
	post_code = models.CharField(max_length=8, null=True, blank=True)
	country = models.CharField(max_length=100, null=True, blank=True)
	longitude = models.CharField(max_length=50, null=True, blank=True)
	latitude = models.CharField(max_length=50, null=True, blank=True)

	captcha_score = models.FloatField(default = 0.0)
	has_profile = models.BooleanField(default = False)
	
	is_active = models.BooleanField(default = True)

	def __str__(self):
		return f'{self.user}'


class Venue(models.Model):

    name = models.CharField(max_length=255)

    latitude = models.DecimalField(
                max_digits=9, decimal_places=6, null=True, blank=True)

    longitude = models.DecimalField(
                max_digits=9, decimal_places=6, null=True, blank=True)


