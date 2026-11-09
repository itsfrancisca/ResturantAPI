from django.shortcuts import render

# Create your views here.



from rest_framework import viewsets, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Category, MenuItem, order, OrderItem
from .serializers import (UserRegistrationSeriallizer, CategorySerializer, MenuItemSerializer, orderSerializer)

# Create your views here.

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSeriallizer
    permission_classes = [permissions.AllowAny]

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        self.response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=self.response.data['token'])
        user = token.user
        return Response({
            'token' : token.key,
            'user_id' : user.pk,
            'username' : user.username,
            'is_staff' : user.is_staff
        })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return[permissions.AllowAny()]
        return super().get_permissions()


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ['category', 'is_available']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all()
    serializer_class = orderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')
