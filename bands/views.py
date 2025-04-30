from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from  bands.models import Musician, Band,Venue

def musician(request,musician_id):
    musician = get_object_or_404(Musician,id= musician_id)
    data ={
        'musician': musician,
    }
    return render(request,'musician.xhtml',data)

def musicians(request):

    all_musicians = Musician.objects.all().order_by('last_name')
    paginator = Paginator(all_musicians, 2)

    page_num = request.GET.get('page',1)
    page_num = int(page_num)

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)
    data = {
        'musicians': page.object_list,
        'page': page
    }
    return render(request,'musicians.xhtml',data)

def band(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    data = {
        'band': band,
    }
    return render(request, 'bands.xhtml', data)

def bands(request):
    all_bands = Band.objects.all().order_by('name')
    paginator = Paginator(all_bands, 2) 

    page_num = request.GET.get('page', 1)
    page_num = int(page_num)

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)
    data = {
        'bands': page.object_list,
        'page': page
    }
    return render(request, 'bands.xhtml', data)

def venues(request):
    all_venues = Venue.objects.all().order_by('name')
    data = {
        'venues': all_venues,
    }
    return render(request, 'venues.xhtml', data)