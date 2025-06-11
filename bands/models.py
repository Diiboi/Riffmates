from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth = models.DateField()
    description = models.TextField(blank=True, null=True, help_text="A brief biography of the musician")
    bio_pic = models.ImageField(
        upload_to='musicians/bio_pics/',
        blank=True,
        null=True,
        help_text="Profile picture of the musician"
    )
    user_profile = models.ForeignKey(
        'UserProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='musicians',
        help_text="The user profile that owns this musician record"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Musician'
        verbose_name_plural = 'Musicians'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('musician', kwargs={'musician_id': self.id})

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    full_name.short_description = 'Full Name'

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birth).days / 365.25)
    age.short_description = 'Age'
    
    
class Venue(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    picture = models.ImageField(blank=True,null=True)
    def __str__(self):
        return f"Venue(id={self.id}, name={self.name})"
    
class Room(models.Model):
    name=models.CharField(max_length=20)
    Venue=models.ForeignKey(Venue, on_delete=models.CASCADE)
    def __str__(self):
        return f"Room(id={self.id}, name={self.name}, Venue={self.Venue})"
class Band(models.Model):
    name = models.CharField(max_length=50)
    musicians=models.ManyToManyField(Musician)
    def __str__(self):
        return f"Band(id={self.id}, name={self.name})"
    
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    musician_profiles=models.ManyToManyField(Musician,blank=True)
    venue_controlled=models.ManyToManyField(Venue,blank=True)