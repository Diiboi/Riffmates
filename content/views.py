from django.core.mail import send_mail
from django.shortcuts import render, redirect,get_object_or_404
from content.models import MusicianBandChoice,SeekingAd
from django.contrib.auth.decorators import login_required
from content.forms import SeekingAdForm
from content.models import MusicianBandChoice,SeekingAd
from content.forms import CommentForm

@login_required
def comment(request):
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            message = f"""\
            Recieved comment from {name}\n\n
            {comment}
            """
            send_mail("Recieved comment", message, 'admin@example.com', ['admin@example.com'], fail_silently=False)
            return redirect('comment_accepted')
    data={
        "form":form,
    }
    return render(request, 'comment.html', data)

def comment_accepted(request):
    data ={
        "content":"""
        <h1> Comment accepted</h1>
        <p>Thank you for your comment to <i>Riffmates</i></p>
        """
    }
    return render(request, 'general.xhtml', data)

@login_required
def list_ads(request):
    data ={
        'seeking_musician':SeekingAd.objects.filter(seeking=MusicianBandChoice.MUSICIAN),
        'seeking_band':SeekingAd.objects.filter(seeking=MusicianBandChoice.BAND),
    }
    return render(request, 'list_ads.html', data)

@login_required
def seeking_ad(request, ad_id=0):
    ad = None
    
    # Get the ad instance if editing
    if ad_id != 0:
        ad = get_object_or_404(SeekingAd, id=ad_id)
        # Check permissions - owner or staff
        if not (request.user == ad.owner or request.user.is_staff):
            raise Http404("Permission denied")
    
    # Handle form submission
    if request.method == 'POST':
        form = SeekingAdForm(request.POST, instance=ad)
        if form.is_valid():
            ad = form.save(commit=False)
            # Only set owner for new ads (don't override on edit)
            if ad_id == 0:
                ad.owner = request.user
            ad.save()
            return redirect('list_ads')
    else:
        # GET request - initialize form
        form = SeekingAdForm(instance=ad)
    
    context = {
        "form": form,
        "ad": ad,  # Pass the ad object to template
        "is_new": ad_id == 0  # Helpful for template logic
    }
    return render(request, "seeking_ad.html", context)
   