from django.shortcuts import render,get_object_or_404,redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from  bands.models import Musician, Band,Venue,UserProfile
from bands.forms import VenueForm,MusicianForm


@login_required 
def restricted_page(request):
    data={
        'title':'Restricted Page',
        'content':'<h1> You are logged in</h1>',
    }
    return render(request,"general.xhtml",data)

@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    profile = request.user.userprofile
    allowed = False
    
    if profile.musician_profiles.filter(id=musician_id).exists():
        allowed = True
    else:
        user_musicians = set(profile.musician_profiles.all())
        for band in musician.band_set.all():
            band_musicians = set(band.musicians.all())
            if user_musicians.intersection(band_musicians):
                allowed = True
                break
    
    if not allowed:
        raise Http404("Permission denied")
    
    content = f"""
    <h1> Musician Page: {musician.last_name}</h1>
    <p> {musician.first_name}</p>
    <p> {musician.last_name}</p>
    <p> {musician.birth}</p>
    """
    data = {
        'title': 'Musician Restricted',
        'content': content,
    }
    return render(request, 'general.xhtml', data)



@login_required
def musician(request,musician_id):
    musician = get_object_or_404(Musician,id= musician_id)
    can_edit = False
    
    if request.user.is_authenticated:
        if request.user.is_staff or (hasattr(request.user, 'userprofile') and 
                                   request.user.userprofile.musicians.filter(id=musician_id).exists()):
            can_edit = True
    
    return render(request, 'musician.xhtml', {
        'musician': musician,
        'can_edit': can_edit
    })

@login_required
def edit_musician(request, musician_id=None):
    musician = None
    if musician_id:
        musician = get_object_or_404(Musician, id=musician_id)
        if not (request.user.is_staff or 
               request.user.userprofile.musicians.filter(id=musician_id).exists()):
            raise Http404("Permission denied")

    if request.method == 'POST':
        form = MusicianForm(request.POST, request.FILES, instance=musician)
        if form.is_valid():
            musician = form.save(commit=False)
            if not musician_id:  
                musician.user_profile = request.user.userprofile
            musician.save()
            return redirect('musician', musician_id=musician.id)
    else:
        form = MusicianForm(instance=musician)

    return render(request, 'edit_musician.html', {
        'form': form,
        'musician': musician
    })


def musicians(request):

    all_musicians = Musician.objects.all().order_by('last_name')
    paginator = Paginator(all_musicians, 4)

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
    musicians = band.musicians.all().order_by('last_name', 'first_name')  # Get all musicians in this band
    
    data = {
        'band': band,
        'musicians': musicians,  # Pass the musicians queryset to the template
        'member_count': musicians.count(),  # Pass the count for easy display
    }
    return render(request, 'band_desc.xhtml', data)

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

@login_required
def edit_venue(request, venue_id=0):
    venue = None  # Initialize venue as None by default
    
    if venue_id != 0:
        venue = get_object_or_404(Venue, id=venue_id)
        if not request.user.userprofile.venue_controlled.filter(id=venue_id).exists():
            raise Http404("Can only edit controlled venues")

    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            venue = form.save()
            if venue_id == 0:  # Only add to controlled venues if new
                request.user.userprofile.venue_controlled.add(venue)
            return redirect('venues')
    else:
        form = VenueForm(instance=venue)

    return render(request, 'edit_venue.xhtml', {
        'form': form,
        'venue': venue,  # Now always defined
        'is_new': venue_id == 0  # Additional context variable
    })

def _get_items_per_page(request):
    # Determine how many items to show per page, disallowing <1 or >50
    items_per_page = int(request.GET.get("items_per_page", 10))
    if items_per_page < 1:
        items_per_page = 10
    if items_per_page > 50:
        items_per_page = 50
    return items_per_page

def _get_page_num(request, paginator):
    # Get current page number for Pagination, using reasonable defaults
    page_num = int(request.GET.get("page", 1))
    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages
    return page_num


def venues(request):
    all_venues = Venue.objects.all().order_by("name")
    profile = getattr(request.user, "userprofile", None)
    
    if profile:
        for venue in all_venues:
            # Mark the venue as "controlled" if the logged in user is
            # associated with the venue
            venue.controlled = profile.venue_controlled.filter(
                id=venue.id
            ).exists()
    else:
        # Anonymous user, can't be associated with the venue
        for venue in all_venues:
            venue.controlled = False

    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_venues, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)

    data = {
        "venues": page.object_list,
        "page": page,
    }
    return render(request, "venues.xhtml", data)


@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
        if kwargs['created'] and not kwargs['raw']:
            user = kwargs['instance']
            try:
                UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
                
                
