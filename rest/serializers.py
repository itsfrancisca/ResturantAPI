from rest_framework  import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Category, MenuItem, order, OrderItem


class UserRegistrationSeriallizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        models =User
        fields = ['id','usernmae', 'email', 'password']


        def create(self,validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['passwoed']
            )
            Token.objects.create(user=user)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        models = MenuItem
        fields = '__all__'


class orderSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_items.name')

    class Meta:
        model = OrderItem
        fields = ['id',  'menu_item', 'menu_item_name', 'quantity', 'prioce']

    def create(self, validated_date):
        request = self.context.get('request')
        items_data = self.validated_data.prop('items')

        order = Order.objects.create(user=request.user, **validated_data)

        total = 0
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            item_price = menu_item.price * quantity
            total += item_price

            OrderItem.objects.create(
                order = order,
                menu_item = menu_item,
                quantity = quantity,
                price = menu_item.price
            )

        order.total_price = total
        order.save()
        return order