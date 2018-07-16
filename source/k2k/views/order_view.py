from django.conf.urls import url
from k2k.models import *
from django.shortcuts import render, render_to_response, redirect
from debugalize.tools import tools, jqgrid
from django.contrib.auth.decorators import login_required
import logging
import sys
import os
from django.template.context_processors import request
log = logging.getLogger(__name__)

def sub_cat_admin(request):
    context = tools.defaultContextData(request)
    return render_to_response('admin/order/order.html', context)

def order_get_data(request):
    def dict_annotation(d, o):
        d['user'] = o.User.username
    items_list = jqgrid.get_jqgrid_data_json(request, Order, None, "GET", None, None)
    return tools.ajax_response(items_list) 

def order_item_page (request):
    ctx = tools.defaultContextData(request)
    order_id = request.GET.get('id')
    order = Order.objects.filter(id = order_id ).first() 
    ctx['order'] = order
    
    #data = jqgrid.get_jqgrid_data_json(request, Order, None, "GET", None, None)
    #ctx['data'] = data
    return render_to_response("admin/order/Order_Item.html", ctx)




#===============================================================================
# URLs
#===============================================================================
urls = [
    url(r'^$', sub_cat_admin, name='order'),
    url(r'^admin_order',order_get_data,name='get_order_data'),
    url(r'^order_item_page',order_item_page,name='order_item_page')
]   