from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

def home_page(request):
    if request.method == 'POST':
        return render(request, 'lists/home.html' ,
               {'new_item_text': request.POST.get('item_text','')})
    return render(request, 'lists/home.html',{})

