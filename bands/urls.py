from django.urls import path
from bands import views
urlpatterns = [
    path('musician/<int:musician_id>/', views.musician, name='musician'),
    path('musicians/', views.musicians, name='musicians'),
    path('bands/', views.bands, name='bands'),
    path('band/<int:band_id>/', views.band, name='band'),
    path('venues/', views.venues, name='venues'),
    path('musician_restricted/<int:musician_id>/',views.musician_restricted,  name='musician_restricted'),
]
