import json

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, FAQ
from order.models import ShopCart
from product.models import Product, Category, Restaurant, Comment


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category=Category.objects.all()
    dayproducts=Product.objects.all()[:4]
    lastproducts=Product.objects.all().order_by('-id')[:4]
    randomrestaurants=Restaurant.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    context={
        'setting':setting,
        'category':category,
        'page': 'home',
        'sliderdata':sliderdata,
        'dayproducts':dayproducts,
        'lastproducts':lastproducts,
        'randomrestaurants':randomrestaurants
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
    setting = Setting.objects.get(pk=1)
    restaurant = Restaurant.objects.all()
    context = {'setting':setting,
               'restaurant': restaurant,
               }
    return render(request, 'restaurants.html', context)

def restaurant_products(request,id):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products=Product.objects.filter(restaurant_id=id).order_by('category_id')
    context={'setting':setting,
             'products':products,
             'category':category
             }
    return render(request, 'restaurant_products.html',context)

def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)

            #return HttpResponse(products)
            context = {'products' : products,
                       'category' : category,
                       }
            return render(request,'products_search.html',context)

    return HttpResponseRedirect('/')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term','')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Hatalı giriş!')
            return HttpResponseRedirect('/login')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'category': category,
               'setting':setting,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request,user)
            return HttpResponseRedirect("/")
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form':form,
               }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {
        'category':category,
        'faq':faq,
    }
    return render(request, 'faq.html',context)