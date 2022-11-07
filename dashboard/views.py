from django.shortcuts import render

from utils.custom_viewset import CustomViewSet
from utils.response_wrapper import ResponseWrapper
from .serializers import *
from .models import *

from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework.authtoken.serializers import AuthTokenSerializer

# Create your views here.


class CategoryViewSet(CustomViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'


class ProductViewSet(CustomViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

    def product_details(self, request,id, *args, **kwargs):
        qs = Product.objects.filter(id = id).last()
        if not qs:
            return ResponseWrapper(error_msg='Product Not Found', status=400)
        
        serializer  = ProductDetailsSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)


class LoginView(CustomViewSet):

    def get_serializer_class(self):
        if self.action == ['post']:
            self.serializer_class = AuthTokenSerializer

        else:
            self.serializer_class = AuthTokenSerializer

        return self.serializer_class


    def post(self, request):
        email = request.data['username']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            # raise AuthenticationFailed('User not found!')
            return ResponseWrapper(error_msg='User Not Found', status=400)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'name': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = ResponseWrapper(status=200)

        response.set_cookie(key='jwt', value=token, httponly=True)
        # print(user)

        response.data = {
            'jwt': token,
            'username': payload
        }
        return response
