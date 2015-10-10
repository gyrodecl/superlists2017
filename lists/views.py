from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})

#ch.10want this view to handle both get and post requests
#post requests to add items to view
def view_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=requested_list,data=request.POST)
        if form.is_valid():
            item = form.save()
            return HttpResponseRedirect(requested_list.get_absolute_url())         
    else:
        form = ExistingListItemForm(for_list=requested_list)
    items = requested_list.item_set.all()
    #print(form)
    return render(request, 'lists/list.html', {'items': items,
                'list': requested_list,
                'form': form})



def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        item = form.save(for_list=list_)
        return HttpResponseRedirect(list_.get_absolute_url())
    else:
        return render(request, 'lists/home.html', {"form": form})


#not using this anymore--refactored to have
#the view_list accept both GET and POST requests
'''
def add_item_to_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    if request.method == 'POST':
        requested_list = List.objects.get(id=list_id)
        text = request.POST['text']
        Item.objects.create(text=text,list=requested_list)
        return HttpResponseRedirect(reverse('lists:view_list', args=(requested_list.id,)))
    else:
        return HttpResponseRedirect(reverse('lists:view_list', args=(requested_list.id,)))
''' 