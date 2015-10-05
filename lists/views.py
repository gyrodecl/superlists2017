from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from lists.models import Item

def home_page(request):
    return render(request, 'lists/home.html', {})

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html' ,
               {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return HttpResponseRedirect(reverse('lists:view_list'))
