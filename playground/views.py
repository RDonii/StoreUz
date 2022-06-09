from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Collection, Customer, Address, Promotion, Cart, CartItem
from tags.models import TaggedItem
import random

def homeview(request):
    obj_type = random.choice([Product, Collection, Customer, Address, Promotion, Cart, CartItem])
    result = TaggedItem.objects.get_tags_for(obj_type, random.randint(0, 1000))
    
    return render(request, 'index.html', {'result': result})