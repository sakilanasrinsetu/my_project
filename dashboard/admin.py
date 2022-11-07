from unicodedata import category
from django.contrib import admin
from .models import Category, Product, UserProfile, Venue


from django.conf import settings

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

admin.site.register(UserProfile)


