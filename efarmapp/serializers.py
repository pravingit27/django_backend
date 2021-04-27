from rest_framework import serializers
from .models import Category,Product,cart,Admin,order,calory
#from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.serializers import Serializer

class ProductAdminSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ('name',)

class RegisterSerializer(serializers.ModelSerializer):
	products = ProductAdminSerializer(many=True,read_only=True)
	#products = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
	#products = serializers.ReadOnlyField(many=True,source='product.name')
	def create(self, validated_data):
		password = validated_data.pop('password',None)
		instance = self.Meta.model(**validated_data)

		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

	def update(self, instance, validated_data):
	   for attr, value in validated_data.items():
		   if attr == 'password':
			   instance.set_password(value)
		   else:
			   setattr(instance,attr,value)
	   instance.save()
	   return instance

	class Meta:
		model = Admin
		#extra_kwargs = {'products':{'write only':True}}
		fields = ('name','email','password','phone_number','farm_name','username','products')
	   

class CategorySerializer(serializers.ModelSerializer):
   
   class Meta:
	   fields = (
		   'id',
		   'title'
	   )
	   model = Category

#class ProductUserSerializer(serializers.ModelSerializer):
 #   class Meta:
  #      model = User
   #     fields = ('username')

	#def method(self, obj):
	 #   return obj.username

class ProductSerializer(serializers.ModelSerializer):
	#created_by = ProductUserSerializer(read_only=True,many=False)
	#created_by = serializers.ReadOnlyField(source='created_by.username')
	#category = serializers.CharField(source ='category.title')
	image = serializers.ImageField(max_length=None,allow_empty_file=False,allow_null=True,required=False)

	class Meta:
		fields = (
			#'id',
			'name',
			#'slug',
			'category',
			'price',
			'quantity',
			'image',
			'owner',
			'date_created'
		)
		model = Product

	def to_representation(self,instance):
		product = super(ProductSerializer,self).to_representation(instance)
		product['category'] = instance.category.title
		return product
			   

#class UserSerializer(serializers.ModelSerializer):
	#products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
	
  #  class Meta:
   #     model = User
	#    fields = (
	 #        'id',
	  #       'username',
	   #      'email',
		#     'products',
		#)

#class CartUserSerializer(serializers.ModelSerializer):
	
 #   class Meta:
  #      model = User
   #     fields = ('username','email')

class CartSerializer(serializers.ModelSerializer):
	#cart_id = CartUserSerializer(read_only=True, many=False)
	products = ProductSerializer(read_only=True, many=True)

	class Meta:
		model = cart
		fields = (
			'cart_id',
		   # 'created_at',
			'products',
		)



class OrderSerializer(serializers.HyperlinkedModelSerializer):
  
	class Meta:
		model = order
		fields=('id','name','city','address','phone_num','product_names','price','product_quantity','sub_total','final_total')

		def create(self, validated_data):
			product_data = validated_data.pop('product_names')  
			contact = order.objects.create(**product_data)
			product = order.objects.create(product_names=contact, **validated_data)
			return order
			

class CalorySerializer(serializers.ModelSerializer):
	class Meta:
		model = calory

		fields = ('name','serving','calories')