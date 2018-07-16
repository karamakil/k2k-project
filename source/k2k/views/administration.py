from django.conf.urls import url
from k2k.models import Item, Category, SubCategory, Size, ItemMedia , Color
from django.shortcuts import render, render_to_response, redirect
from debugalize.tools import tools, jqgrid
from django.contrib.auth.decorators import login_required
import logging
import sys
import os
from django.template.context_processors import request
from k2k.tools import k2k_tools
from k2k import settings
from turtledemo.nim import COLOR
from django.core.management import color
log = logging.getLogger(__name__)
from django.db.models import Q

#@login_required(login_url='/administration/login')

 

def index(request):
    context = tools.defaultContextData(request)
    return render_to_response('admin/item/items_list.html', context)

def get_items_data(request):
    
    def dict_annotation(d, o):
        d['category'] = o.category.name
        d['sub_category'] = o.sub_category.name
        
        item_media = ItemMedia.objects.filter(item=o).first()
        d['item_img'] =  "%s%s" % (settings.MEDIA_URL, item_media.media_path) if item_media else ""
        
        return d
    base_f = Q(is_new= True)
    
    items_list = jqgrid.get_jqgrid_data_json(request, Item, base_f, "GET", None, dict_annotation)
    return tools.ajax_response(items_list)


#this function is used for checking if its for editing or adding
def get_item_form_page(request):
    ctx = tools.defaultContextData(request)
  
    if request.GET.get('id'):
        item = Item.objects.filter(id=request.GET["id"]).first()
        ctx['item'] = item  
        ctx['operation'] = 'edit'
        
        ctx['selected_sizes'] = []
        for s in item.sizes.all():
            ctx['selected_sizes'].append(s.id)
        
        item_media = ItemMedia.objects.filter(item=item).first()
        ctx['item_img'] =  "%s%s" % (settings.MEDIA_URL, item_media.media_path) if item_media else ""
       
    else:
        #ctx['item'] = Item()
        ctx['operation'] = 'add'
        
    ctx['categories'] = Category.objects.filter()
    ctx['subcategory'] = SubCategory.objects.filter()
    ctx['sizes_list'] = Size.objects.filter()
    ctx['color'] = Color.objects.filter()
    
    return render_to_response('admin/item/item_form.html', ctx); 

def post_delete_item(request):
    result = {'status': "FAIL"}
    
    item_id = request.POST['item_id']
    
    #logic of deleting an item
    Item.objects.filter(id=item_id).delete()
    
    result = {'status': "SUCCESS"}
    return tools.ajax_response(result)



def post_item_form_page(request):
    
    operation = request.POST['oper'] 
    if operation == "add":
        item = Item()
    else:
        item = Item.objects.filter(id=request.POST['id']).first()
   
    item.category_id = request.POST['category']
    item.sub_category_id = request.POST['sub_category']
    item.name = request.POST['name']     
    item.quantity = request.POST['quantity']
    item.price = float(request.POST['price']) if request.POST['price'] else 0
    item.discount = float(request.POST['discount']) if request.POST['discount'] else 0
    
    #item.colors = request.POST['color']
    item.description = request.POST['description']     
    item.save()
     
    item.sizes.set([])
    #list of sizes ids
    seleted_sizes_ids = request.POST.getlist('seleted_sizes')
    for s_id in seleted_sizes_ids:
        size_obj = Size.objects.filter(id=s_id).first()
        item.sizes.add(size_obj)
        
    item.colors.set([])   
    seleted_color_ids = request.POST.getlist('seleted_color')
    for c_id in seleted_color_ids:
        color_obj = Color.objects.filter(id = c_id).first()
        item.colors.add(color_obj)
        
    item.save()
   
    
       
    image_file = request.FILES.get('image_file')
    if image_file:
        #large image path
        image_path = "Items/%s.png" % (item.id)
        full_path = "%s/%s" % (settings.MEDIA_ROOT, image_path) 
        
        k2k_tools.store_media_on_disk(image_file, full_path)
        
        ItemMedia.objects.filter(item=item).delete()
        ItemMedia.objects.create(
            item = item,
            media_type = ItemMedia.IMAGE_TYPE,  
            media_path = image_path,
            is_preview = True
        )
        
    return redirect('items')


urls = [
    # items
    url(r'^$', index , name='items'),
    url(r'^get_items_data', get_items_data, name='items_data'),
    url(r'^item_form$', get_item_form_page, name='item_form'),
    url(r'^post_item_form$', post_item_form_page, name='post_item_form'),
    url(r'^post_delete_item', post_delete_item, name='delete_item'),
    
    
   
  
  # url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'admin/authentication/login_page.html', 'extra_context': {'next':'/administration'}}, name="login"),
    #url(r'^logout$', django_views.logout, {'next_page':'/administration/login'}, name="admin_logout_url"),
  
]

