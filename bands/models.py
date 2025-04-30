from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth=models.DateField()
def __str__(self):
    return f"Musiciane(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, birth={self.birth})"

class Venue(models.Model):
    name = models.CharField(max_length=50)
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
    