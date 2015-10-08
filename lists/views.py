from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})

#ch.10want this view to handle both get and post requests
#post requests to add items to view
def view_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try: 
            item = Item(text=request.POST['item_text'], list=requested_list)
            item.full_clean()
            item.save()
            return HttpResponseRedirect(requested_list.get_absolute_url())   
        except ValidationError:
            error = "You can't have an empty list item"
    items = requested_list.item_set.all()
    return render(request, 'lists/list.html',
               {'items': items,
                'list': requested_list,
                'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
        print("here")
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {'error': error})
    return HttpResponseRedirect(list_.get_absolute_url())


#not using this anymore--refactored to have
#the view_list accept both GET and POST requests
'''
def add_item_to_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    if request.method == 'POST':
        requested_list = List.objects.get(id=list_id)
        text = request.POST['item_text']
        Item.objects.create(text=text,list=requested_list)
        return HttpResponseRedirect(reverse('lists:view_list', args=(requested_list.id,)))
    else:
        return HttpResponseRedirect(reverse('lists:view_list', args=(requested_list.id,)))
''' 