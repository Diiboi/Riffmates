from django import forms 
from bands.models import Venue

VenueForm = forms.modelform_factory(Venue,fields =["name","description","picture"])

from django import forms
from .models import Musician

class MusicianForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = ['first_name', 'last_name', 'birth', 'description', 'bio_pic']