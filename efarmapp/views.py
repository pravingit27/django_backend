from django.shortcuts import render
from rest_framework import generics,viewsets,mixins
from rest_framework.permissions import AllowAny
from .models import Category,Product,cart,Admin,order,calory
from django.contrib.auth.models import User
from .serializers import CategorySerializer,ProductSerializer,CartSerializer,RegisterSerializer,OrderSerializer,CalorySerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth import login,logout
import re
#from rest_framework import permissions
import random

def generate_session_token(length=10):
	return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)] + [str(i) for i in range(10)]) for _ in range(10))

@csrf_exempt
def signin(request):
	if not request.method =='POST':
		return JsonResponse({'error':'send a post request with valid parameter'})
	username = request.POST.get('username')
	password = request.POST.get('password')

	#if not re.match("^[\w\.\+\-]+\0[\w]+\.[a-z]{2,3}$",username):
	#	return JsonResponse({'error':'Enter a valid username'})

	#if usernamevalidation != True:	 
	 #   return "userName is not valid"
	 

	#if len(password)< 4:
	#	return JsonResponse({'error':'password needs to be atleast 4 characters'})

	UserModel = get_user_model()

	try:
	   user = UserModel.objects.get(username = username)

	   if user.check_password(password):
		   user_dict = UserModel.objects.filter(username = username).values().first()
		   user_dict.pop('password')

		   if user.session_token != "0":
			   user.session_token = "0"
			   user.save()
			   return JsonResponse({'error':'previous token exists'})
			
		   token = generate_session_token()
		   user.session_token = token
		   user.save()
		   login(request,user)
		   return JsonResponse({'token':token,'user':user_dict})

	   else:
		   return JsonResponse({'errors':'not logged in'})
					   
	except UserModel.DoesNotExist:
		return JsonResponse({'error':'Invalid username'})

def signout(request,username):
	logout(request)

	UserModel = get_user_model()

	try:
		user = UserModel.objects.get(pk=username)
		user.session_token = "0"
		user.save()

	except UserModel.DoesNotExist:
		return JsonResponse({'error':'invalid user name'})
	
	return JsonResponse({'success':'logout success'})

class ListAdmin(viewsets.ModelViewSet):
	permission_classes_by_action = {'create':[AllowAny]}

	queryset = Admin.objects.all()
	serializer_class = RegisterSerializer

	def get_permissions(self):
		try:
			return [permission() for permission in self.permission_classes_by_action[self.action]]

		except KeyError:
			return[permission() for permission in self.permission_classes]


class ListCategory(generics.ListCreateAPIView):
 #   permission_classes = (permissions.IsAuthenticated,)
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class DetailCategory(generics.RetrieveUpdateDestroyAPIView):
  #  permission_classes = (permissions.IsAuthenticated,)
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class ListProduct(generics.ListCreateAPIView):
   # permission_classes = (permissions.IsAuthenticated,)
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class DetailProduct(generics.RetrieveUpdateDestroyAPIView):
	#permission_classes = (permissions.IsAuthenticated,)
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

	3#@action(methods=['get'], detail=False,
	  #      url_path='products/(?P<name>\w+)')
	#def getByUsername(self, request, name):
	 #   product = get_object_or_404(Product, name=name)
	  #  data = ProductSerializer(product).data
	   # return Response(data, status=status.HTTP_200_OK)

	#lookup_field = 'slug'

#class ListUser(generics.ListCreateAPIView):
#	#permission_classes = (permissions.IsAuthenticated,)
#	queryset = User.objects.all()
#	serializer_class = UserSerializer

#class DetailUser(generics.RetrieveUpdateDestroyAPIView):
	#permission_classes = (permissions.IsAuthenticated,)
#	queryset = User.objects.all()
#	serializer_class = UserSerializer

class ListCart(generics.ListCreateAPIView):
	#permission_classes = (permissions.IsAuthenticated,)
	queryset = cart.objects.all()
	serializer_class = CartSerializer

class DetailCart(generics.RetrieveUpdateDestroyAPIView):
	#permission_classes = (permissions.IsAuthenticated,)
	queryset = cart.objects.all()
	serializer_class = CartSerializer

#def add(request):
#	if request.method == 'POST':
#		transaction_id = request.POST['order_id']
##		products = request.POST['products']
#		seller = request.POST['seller']
#
#		total_pro = len(products.split(','[:-1]))

#		ordr = order(product_names=products,total_product=total_pro,order_id=transaction_id,total_amount=amount,owner=seller)
#		ordr.save()
#		return JsonResponse({'success':True,'error':False,'msg':'order Placed Successfully'})


class ListOrder(generics.ListAPIView):
	"""This view provides list, detail, create, retrieve, update
	and destroy actions for Products."""
	queryset = order.objects.all()
	serializer_class = OrderSerializer
	lookup_field = 'id'


class DetailOrder(generics.RetrieveUpdateDestroyAPIView):
	queryset = order.objects.all()
	serializer_class = OrderSerializer
	lookup_field = 'id'

class ListCalories(generics.ListCreateAPIView):
	queryset = calory.objects.all()
	serializer_class = CalorySerializer

	def get_serializer(self, *args, **kwargs):
		if "data" in kwargs:
			data = kwargs["data"]

		# check if many is required
			if isinstance(data, list):
				kwargs["many"] = True

		return super(ListCalories, self).get_serializer(*args, **kwargs)

class DetailCalories(generics.RetrieveUpdateDestroyAPIView):
	queryset = calory.objects.all()
	serializer_class = CalorySerializer

	

	