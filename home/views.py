from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from home.models import Setting, ContactFormu


def index(request):
    setting = Setting.objects.get(pk=1)
    context={'setting':setting,'page': 'home'}
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