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
    return render_to_response('admin/subcategory/sub_cat.html', context)

    
def SubCategory_get_data(request):
     
    def dict_annotation(d, o):
        d['category'] = o.category.name
        return d
    items_list = jqgrid.get_jqgrid_data_json(request, SubCategory, None, "GET", None, dict_annotation)
    return tools.ajax_response(items_list) 

def get_SubCategory_form_page(request):
    ctx = tools.defaultContextData(request)
  
    if request.GET.get('id'):
        ctx['subcategory'] = SubCategory.objects.filter(id=request.GET["id"]).first()
        ctx['operation'] = 'edit'
    else:
        ctx['operation'] = 'add'
        
    ctx['categories'] = Category.objects.filter()
    
    return render_to_response('admin/subcategory/sub_cat_item_form.html', ctx);  

def post_SubCategory_form_page(request):
    operation = request.POST['oper'] 
    if operation == "add":
        subcat = SubCategory()
    else:
        subcat = SubCategory.objects.filter(id=request.POST['id']).first()
    
    subcat.name = request.POST['name']
    subcat.category_id = request.POST['category']    
    subcat.save()
    return redirect('sub_cat_admin') 


def post_delete_sub_category(request):
    result = {'status': "FAIL"}
    item_id = request.POST['item_id']
    #logic of deleting an item
    SubCategory.objects.filter(id=item_id).delete()
    result = {'status': "SUCCESS"}
    return tools.ajax_response(result)

#===============================================================================
# URLs
#===============================================================================
urls = [
    url(r'^$', sub_cat_admin, name='sub_cat_admin'),
    url(r'^sub_cat_admin_data', SubCategory_get_data, name='subcat_data'),
    url(r'^sub_cat_item_form$', get_SubCategory_form_page, name='sub_cat_item_form'),
    url(r'^post_subcat_form$', post_SubCategory_form_page, name='post_subcat_form'),
    url(r'^post_delete_sub_category$', post_delete_sub_category, name='post_delete_sub_category'),
   
]