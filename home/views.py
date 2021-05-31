from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from home.models import Setting, ContactFormu
from product.models import Product, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category=Category.objects.all()

    context={
        'setting':setting,
        'category':category,
        'page': 'home',
        'sliderdata':sliderdata
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