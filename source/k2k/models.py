from django.db import models

    
class Country(models.Model):
    name = models.CharField(max_length=128)
    
    
class Category(models.Model):
    name = models.CharField(max_length=128)
    image_path = models.CharField(max_length=128, null=True, default=None)


class SubCategory(models.Model):
    name = models.CharField(max_length=128)
    image_path = models.CharField(max_length=128, null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, default=None)
    
 
class Size(models.Model):
    name = models.CharField(max_length=128)
    
    
class Color(models.Model):
    name = models.CharField(max_length=128)
    

class Item(models.Model):
    name = models.CharField(max_length=128, null=True)
    price = models.FloatField(null=True, default=None)
    discount = models.FloatField(null=True, default=None)
    description = models.TextField(null=True)
    available_quantity = models.IntegerField(default=0)
    is_new = models.BooleanField(default=False) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, default=None)
    colors = models.ManyToManyField(Color, null=True, default=None)
    sizes = models.ManyToManyField(Size, null=True, default=None)


class ItemMedia(models.Model):
    IMAGE_TYPE = "image"
    VIDEO_TYPE    = "video"
     
    MEDIA_TYPES_LIST = (
        (IMAGE_TYPE, "Image"),
        (VIDEO_TYPE, "Video"),
    )

    media_type = models.CharField(max_length=128, choices=MEDIA_TYPES_LIST)
    media_path = models.CharField(max_length=128)
    is_preview = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class User(models.Model):
    username = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    phone = models.IntegerField()
    user_address = models.CharField(max_length=128)
    
    
class Order(models.Model):
    created_ts = models.DateTimeField()
    delivery_ts=models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, default=None)
    

class OrderItem(models.Model):
    quantity = models.IntegerField(default=0)    
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)



    
    
    
    
#  category = models.CharField(max_length=16, null=True , choices=CATEGORIES_LIST)
#    TSHIRT = "Tshirt"
#     JEANS    = "jeans"
#     SHOES = "shoes"
#     
#     CATEGORIES_LIST = (
#        (TSHIRT, "Tshirt"),
#        (JEANS, "Jeans"),
#        (SHOES, "Shoes"),
#     )
    