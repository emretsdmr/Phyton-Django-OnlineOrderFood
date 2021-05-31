from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from home.models import Setting, ContactFormu
from product.models import Product, Category, Restaurant, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category=Category.objects.all()
    dayproducts=Product.objects.all()[:4]
    lastproducts=Product.objects.all().order_by('-id')[:4]
    randomproducts=Product.objects.all().order_by('?')[:4]


    context={
        'setting':setting,
        'category':category,
        'page': 'home',
        'sliderdata':sliderdata,
        'dayproducts':dayproducts,
        'lastproducts':lastproducts,
        'randomproducts':randomproducts
    }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context={'setting':setting}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context={'setting':setting}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):
    if request.method=='POST':
        form=ContactFormu(request.POST)
        #return HttpResponse(form.data['name'])
        if form.is_valid():
            form = ContactFormu(request.POST)
            form.name = form.data['name']
            form.subject = form.data['subject']
            form.email = form.data['email']
            form.message = form.data['message']
            form.ip = request.META.get('REMOTE_ADDR')
            form.save()
            messages.success(request,'Mesajınız başarı ile gönderilmiştir.')
            return HttpResponseRedirect('/iletisim')


    setting = Setting.objects.get(pk=1)
    form= ContactFormu()
    context={'setting':setting,'form':form}
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    setting = Setting.objects.get(pk=1)
    categorydata = Category.objects.get(pk=id)
    category=Category.objects.all()
    products=Product.objects.filter(category_id=id)
    context={'setting':setting,
             'category':category,
             'products':products,
             'categorydata':categorydata
             }
    return render(request, 'products.html',context)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    restaurant = Product.objects.get(pk=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'category': category,
               'product': product,
               'restaurant':restaurant,
               'comments':comments
               }
    return render(request, 'product_detail.html',context)

def restaurants(request):
    restaurant = Restaurant.objects.all()
    context = {'restaurant': restaurant,
               }
    return render(request, 'restaurants.html', context)

def restaurant_products(request,id):
    setting = Setting.objects.get(pk=1)
    restaurant = Restaurant.objects.get(pk=id)
    products=Product.objects.filter(restaurant_id=id)
    context={'setting':setting,
             'products':products,
             'restaurant':restaurant
             }
    return render(request, 'restaurant_products.html',context)