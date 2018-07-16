from django.conf.urls import url
from django.shortcuts import render_to_response, redirect, render
from debugalize.tools import tools
from k2k.models import *
from django.template.loader import get_template
from k2k import settings
from django.template.context_processors import request
import random



def getMainPage(request):
    ctx = tools.defaultContextData(request)
    
    ctx['items_list'] = Item.objects.filter()[:8]
    for o in ctx['items_list']:
        o.new_price = o.price - ((o.price*o.discount)/100)
    
    # add categories list to the context
    #ctx['categories_list'] =  
    
    #TODO: complete all the values, read the images
    left_values = [136.344, 96.3445, 66.3445, 165.861 , 149.517 , 237.689, 302.689 ,-35.4833, 16.3445,-27.311, 29.5167, -9.13877, 99.5167, 52.689, 120.861, 250.861 , 335.861]
    style_values = ['lg', 'sm', 'med']
    ctx['categories_list'] = SubCategory.objects.filter().order_by('?')[:8]
    for index, cat_obj in enumerate(ctx['categories_list']):
        cat_obj.left = left_values[index] if len(left_values) > index else random.choice(left_values)
        cat_obj.style = random.choice(style_values)
        
    return render_to_response('home.html', ctx);
    
    
def contact_us(request):
    ctx=tools.defaultContextData(request)
    return render_to_response('contact.html',ctx);


def about_us(request):
    ctx=tools.defaultContextData(request)
    return render_to_response('about.html',ctx);


def listing_items(request):
    ctx=tools.defaultContextData(request)
    ctx['items_list']= Item.objects.filter()
    
  #  ctx['total'] = all_quantity()
    
    for i in ctx['items_list']:
        i.new_price = i.price - ((i.price*i.discount)/100)
    return render_to_response('listing.html',ctx);


def all_quantity():
    all['items'] = Item.objects.filter()
    for i in  all['items']:
        i.total_quan=0
        i.total_quan= i.total_quan + i.available_quantity
        return i.total_quan;

        
        


#===============================================================================
# URLs
#===============================================================================

urls = [
    
    url(r'^$', getMainPage,  name='home_page'),    
    url(r'^contact_us',contact_us,name='contact_us' ),
    url(r'^about_us',about_us,name='about_us' ),
    url(r'^shop',listing_items,name='listing' ),
    

]