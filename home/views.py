from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import status
import json
import requests
class BaseView(View):
    views = {}
    views['category'] = Category.objects.filter(status='active')
class HomeView(BaseView):
    def get(self,request):

        self.views['sliders']=Slider.objects.filter(status='active')
        self.views['ads']=Ad.objects.all()
        self.views['brands'] =Brand.objects.filter(status='active')
        self.views['hots']=Item.objects.filter(status='active',label='hot')
        self.views['olds']=Item.objects.filter(status='active',label='old')
        return render(request,'index.html',self.views)
class CategoryItemView(BaseView):
    def get(self,request,slug):
        category_id=Category.objects.get(slug=slug).id
        self.views['cat_items']=Item.objects.filter(category=category_id)
        return render(request,'category.html',self.views)
class BrandItemView(BaseView):
    def get(self,request,slug):
        brand_id=Brand.objects.get(slug=slug).id
        self.views['brand_items']=Item.objects.filter(brand=brand_id)
        return render(request,'category.html',self.views)
class ItemSearchView(BaseView):
    def get(self,request):
        search=request.GET.get('search',None)
        if search is None:
            return redirect('/')
        else:
            self.views['search_item']=Item.objects.filter(name__icontains=search)
            return render(request, 'search.html', self.views)

        return render(request, 'search.html', self.views)

class ItemDetailView(BaseView):
    def get(self, request, slug):
        self.views['item_detail'] = Item.objects.filter(slug=slug)
        return render(request, 'product-detail.html', self.views)

def signup(request):
    if request.method == "POST":
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'This username is already taken')
                return redirect('home:signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'This email is already taken')
                return redirect('home:signup')
            else:
                user=User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=f_name,
                    last_name=l_name,

                )
                user.save()
                messages.success(request,'You have successfully signed up')
                return redirect('home:signup')
        else:
            messages.error(request, 'password do not matches')
            return redirect('home:signup')

    return render(request,'signup.html')

# -----------------------------------------api-------------------------------------------------------------

from rest_framework import routers, serializers, viewsets
# from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404



# ViewSets define the view behavior.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class FilterItemViewSet(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_field=['id','category','label']
    ordering_field=['id','price','title']
    search_field=['title','description']

class ItemDetail(APIView):
    def get_object(selfself,pk):
        try:
            return Item.objects.get(id = pk)
        except:
            raise Http404
    def get(self,request, pk):
        object=self.get_object(pk)
        serializers=ItemSerializer(object,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            pass
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        object=self.get(pk)
        object.delete()
        return Response("The row is deleted.",status=status.HTTP_202_OK)
api_url='http://127.0.0.1:8000/api/item/'
def api_data(request):
    response=requests.get(api_url)
    records=response.text
    records=json.loads(records)
    return render(request,'api.html',{'items':records})