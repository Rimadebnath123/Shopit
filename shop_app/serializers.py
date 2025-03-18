from rest_framework import serializers
from .models import  CartItem, Product, Cart
from django.contrib.auth import get_user_model


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'description',
            'price',
            'category',
        ]

class DetailedProductSerializer(serializers.ModelSerializer):
    similar_products = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "name", "price", "slug", "image", "description", "similar_products"]

    def get_similar_products(self, product):
        products = Product.objects.filter(category= product.category).exclude(id= product.id)
        serializer=ProductSerializer(products, many=True)
        return serializer.data
    
    # def validate_price(self, value):
    #     if value <= 0:
    #         raise serializers.ValidationError("Price must be greater than zero.")
    #     return value

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total=serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product","total"]

    def get_total(self,cartitem):
        price=cartitem.product.price*cartitem.quantity
        return price

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(read_only=True,many=True)
    sum_total=serializers.SerializerMethodField()
    num_of_items=serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_code","items","sum_total","num_of_items","created_at", "modified_at"]

    def get_sum_total(self,cart):
        items=cart.items.all()
        total= sum([item.product.price * item.quantity for item in items])
        return total
    
    def get_num_of_items(self,cart):
        items=cart.items.all()
        total= sum([item.quantity for item in items])
        return total


class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items=serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id", "cart_code", "num_of_items"]

    def get_num_of_items(self,cart):
        num_of_items=sum([item.quantity for item in cart.items.all()])
        return num_of_items
    
class NewCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    order_id = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "order_id", "order_date"]

    def get_order_id(self, cartitem):
        order_id = cartitem.cart.cart_code
        return order_id

    def get_order_date(self, cartitem):
        order_date = cartitem.cart.modified_at
        return order_date


class UserSerializer(serializers.ModelSerializer):
    items=serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "city", "state", "address", "phone","items"]

    def get_items(self, user):
        cartitems = CartItem.objects.filter(cart__user=user, cart__paid=True)[:10]
        serializer = NewCartItemSerializer(cartitems, many=True)
        return serializer.data


class RegisterSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()  # Ensure this is correctly fetching your custom user model
        fields = ["username", "first_name", "last_name", "email", "password", "confirmPassword"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop("confirmPassword")
        user = get_user_model().objects.create_user(**validated_data)  # Use get_user_model()
        return user
