from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime

mock_news = [
    ("2025-04-10", "Breaking News: New Technology Unveiled!"),
    ("2025-04-09", "Sports Update: Local Team Wins Championship"),
    ("2025-04-08", "World Economy: Market Trends and Insights"),
    ("2025-04-07", "Health: The Importance of a Balanced Diet"),
    ("2025-04-06", "Entertainment: Upcoming Movies You Can't Miss"),
    ("2025-04-05", "Weather Alert: Storm Approaching the Coast"),
    ("2025-04-04", "Tech Review: Best Gadgets of 2025"),
    ("2025-04-03", "Politics: New Government Policies Explained"),
    ("2025-04-02", "Lifestyle: How to Stay Productive at Work"),
    ("2025-04-01", "Education: Top Universities for 2025 Admissions"),
]

def home(request):
    paginator = Paginator(mock_news, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

def news_detail(request, id):
    news_item = mock_news[id - 1] 
    return render(request, 'news_detail.html', {'news_item': news_item})

def news_advanced(request):
    paginator = Paginator(mock_news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_adv.html', {'page_obj': page_obj})

def search_results(request):
    query = request.GET.get('q', '')
    filtered_news = [item for item in mock_news if query.lower() in item[1].lower()]
    paginator = Paginator(filtered_news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'search_results.html', {'page_obj': page_obj, 'query': query})


def credits(request):
    content ='tom,jone and john'
    return HttpResponse(content,content_type="text/plain")
def AboutPage(request):
    return JsonResponse(
        {
            'version':'10.1.5',
            'Massage':'Welcome to my website'
            })


