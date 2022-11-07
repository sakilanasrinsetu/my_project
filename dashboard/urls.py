from django.urls import path
from .views import *

urlpatterns = [
     path('category/',
         CategoryViewSet.as_view({'get': 'list','post': 'create'},
                                 name='category')),
     path('category/<pk>/',
         CategoryViewSet.as_view({'get': 'retrieve', 'patch': 'update','delete': 'destroy',},
                                 name='category')),
     path('product/',
         ProductViewSet.as_view({'get': 'list','post': 'create'},
                                 name='category')),
     path('product/<pk>/',
         ProductViewSet.as_view({'get': 'retrieve', 'patch': 'update','delete': 'destroy',},
                                 name='product')),
     path('product_details/<id>/',
         ProductViewSet.as_view({'get': 'product_details'},
                                 name='product_details')),
     path('login/',
         LoginView.as_view({'post': 'post'},
                                 name='post')),

]