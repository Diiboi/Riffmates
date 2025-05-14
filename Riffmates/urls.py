"""
URL configuration for Riffmates project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home import views as home_views
from home import views as about_views
from home import views as homepage_views
from home import views as advanced_views
from home import views as details_views
from home import views as search_views
from bands import views as band_views
urlpatterns = [
    path('bands/',include("bands.urls")),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('credits/',home_views.credits,name='credits'),
    path('about/',about_views.AboutPage,name='about'),
    path('',homepage_views.home,name='home'),
    path('news/advanced/', advanced_views.news_advanced, name='news_advanced'),  
    path('news/<int:id>/', details_views.news_detail, name='news_detail'), 
    path('search/', search_views.search_results, name='search_results'),  
    path('restricted_page/',band_views.restricted_page, name='restricted_page'),
]
