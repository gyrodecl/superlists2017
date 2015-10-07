from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from lists.models import Item, List

def home_page(request):
    return render(request, 'lists/home.html', {})

def view_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    items = requested_list.item_set.all()
    return render(request, 'lists/list.html' ,
               {'items': items,
                'list': requested_list})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
        print("here")
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {'error': error})
    return HttpResponseRedirect(reverse('lists:view_list', args=(list_.id,)))


def add_item_to_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    if request.method == 'POST':
        requested_list = List.objects.get(id=list_id)
        text = request.POST['item_text']
        Item.objects.create(text=text,list=requested_list)
        return HttpResponseRedirect(reverse('lists:view_list', args=(requested_list.id,)))
    else:
        return HttpResponseRedirect(reverse('lists:view_list', args=(requested_list.id,)))
    
