from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id','first_name','last_name','username', 'email']

# Vendor
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        # fields = ['id','user', 'address', 'show_chart_daily_order', 'show_chart_monthly_order', 'show_chart_yearly_order']
        fields = ['id','user','mobile','profile_img','description', 'address', 'show_chart_daily_order', 'show_chart_monthly_order', 'show_chart_yearly_order']
        # fields = ['id','user','address','profile_img']

    
    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ['id','user','mobile','profile_img', 'description', 'address', 'show_chart_daily_order', 'show_chart_monthly_order', 'show_chart_yearly_order','total_products']
    def __init__(self, *args, **kwargs):
        super(VendorDetailSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

# Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id','user', 'mobile']
    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerAddress
        fields = ['id','customer', 'address', 'default_address']
    def __init__(self, *args, **kwargs):
        super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1

class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id','user', 'mobile', 'profile_img','customer_orders']
    # def __init__(self, *args, **kwargs):
    #     super(CustomerDetailSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

#Product

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'product','image']      
        
        
class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=models.ProductCategory.objects.all())
    vendor = serializers.PrimaryKeyRelatedField(queryset=models.Vendor.objects.all())
    product_ratings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = models.Product
        fields = ['id','category', 'vendor', 'title','slug','tag_list', 'detail', 'price', 'usd_price','product_ratings','image','tags','qty']
    def __init__(self, *args, **kwargs):
        super(ProductListSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductRating
        fields = ['id','customer', 'product', 'rating','reviews','add_time']
    def __init__(self, *args, **kwargs):
        super(ProductRatingSerializer, self).__init__(*args, **kwargs)

class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings = serializers.StringRelatedField(many=True, read_only=True)
    product_imgs = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        many = True
        model = models.Product
        fields = ['id','category', 'vendor', 'title', 'slug', 'tag_list', 'detail', 'price', 'usd_price', 'product_ratings', 'product_imgs', 'image', 'tags', 'qty']
    def __init__(self, *args, **kwargs):
        super(ProductDetailSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1






class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id','title', 'detail', 'category_img']
    
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id','title', 'detail']
    def __init__(self, *args, **kwargs):
        super(CategoryDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id','customer','order_status','order_time', 'total_amount', 'total_usd_amount', 'order_address']
    # def __init__(self, *args, **kwargs):
    #     super(OrderSerializer, self).__init__(*args, **kwargs)
    #     self.Meta.depth = 1

class CustomerOrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductDetailSerializer()
    class Meta:
        model = models.OrderItems
        fields = ['id', 'order', 'product', 'qty', 'price', 'usd_price']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItems
        fields = ['id', 'order', 'product', 'qty', 'price','usd_price']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['order'] = OrderSerializer(instance.order).data
        response['customer'] = CustomerSerializer(instance.order.customer).data
        response['user'] = UserSerializer(instance.order.customer.user).data
        response['product'] = ProductDetailSerializer(instance.product).data
        return response



class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItems 
        fields = ['id','order', 'product']
    def __init__(self, *args, **kwargs):
        super(OrderDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wishlist
        fields = ['id','product', 'customer']
    def __init__(self, *args, **kwargs):
        super(WishListSerializer, self).__init__(*args, **kwargs)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data
        response['product'] = ProductDetailSerializer(instance.product).data
        return response


