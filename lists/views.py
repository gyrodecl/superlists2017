from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text','')
        if new_item_text:
            Item.objects.create(text=new_item_text)
            return HttpResponseRedirect(reverse('lists:home'))
    items = Item.objects.all()
    return render(request, 'lists/home.html' ,
               {'items': items})
