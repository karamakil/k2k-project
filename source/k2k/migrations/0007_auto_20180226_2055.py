# Generated by Django 2.0.2 on 2018-02-26 18:55

from django.db import migrations
from k2k.models import SubCategory, Category, Country, Size, Color, Item
import random

def fill_dummy_data(apps, schema_editor):    
    Category.objects.create(name='Men')
    Category.objects.create(name='Women')
       
    Country.objects.create(name='lebanon')
    Country.objects.create(name='turky')
      
    SubCategory.objects.create(name='jeans', category = Category.objects.filter().order_by('?').first(),)
    SubCategory.objects.create(name='t-shirt', category = Category.objects.filter().order_by('?').first(),)
      
    s1 = Size.objects.create(name = 'S')
    s2 = Size.objects.create(name = 'M')
    s3 = Size.objects.create(name = 'L')
      
    c1 = Color.objects.create(name = 'RED')
    c2 = Color.objects.create(name = 'BLUE')
    c3 = Color.objects.create(name = 'GREEM')
                                 
    for i in range(1, 50):
        item = Item(
            name = "item_%s" % (i),
            price = random.randint(1, 50),
            discount = random.randint(1, 50), 
            description = "description_%s" % (i),
            available_quantity = random.randint(1, 50),
            is_new = True if i % 2 == 0 else False,
            category = Category.objects.filter().order_by('?').first(),
            sub_category = SubCategory.objects.filter().order_by('?').first(),
            country = Country.objects.filter().order_by('?').first(),
            )
        item.save()
            
        item.sizes.add(s1)
        item.sizes.add(s2)
        item.sizes.add(s3)
        
        item.colors.add(c1)
        item.colors.add(c2)
        item.colors.add(c3)
        item.save()
        

class Migration(migrations.Migration):

    dependencies = [
        ('k2k', '0006_auto_20180226_2053'),
    ]

    operations = [
        migrations.RunPython(fill_dummy_data),
    ]
