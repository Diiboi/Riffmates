from django.urls import path
from django.contrib.auth import views as auth_views
from bands import views
urlpatterns = [
    path('musician/<int:musician_id>/', views.musician, name='musician'),
    path('musicians/', views.musicians, name='musicians'),
    path('bands/', views.bands, name='bands'),
    path('band/<int:band_id>/', views.band, name='band'),
    path('venues/', views.venues, name='venues'),
    path('musician_restricted/<int:musician_id>/',views.musician_restricted,  name='musician_restricted'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]
