from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from listings.choices import bedroom_choices,price_choices,state_choices

# Create your views here.
def index(request):
    listings = Listing.object.order_by('list_date').filter(is_published=True)[:3]

    context = {
        'listings':listings,
        'state_choices':state_choices,
        'price_choices':price_choices,
        'bedroom_choices':bedroom_choices
    }
    return render(request,'pages/index.html',context)

def about(request):

    realtors = Realtor.object.order_by('hire_date')

    mvp_realtors = Realtor.object.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors,
    }
    return render(request,'pages/about.html',context)
