import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    # ==========================
    # 1) Movies per year chart
    # ==========================
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    graphic_years = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # ==========================
    # 2) Movies per genre chart
    # ==========================
    movies = Movie.objects.values_list('genre', flat=True)
    genre_counts = {}

    for genre in movies:
        if genre:
            first_genre = genre.split(",")[0].strip()  # Tomar solo el primer género
            genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    if genre_counts:  # solo si hay géneros
        plt.bar(genre_counts.keys(), genre_counts.values(), color='skyblue', edgecolor='black')
        plt.title('Movies per Genre')
        plt.xlabel('Genre')
        plt.ylabel('Number of Movies')
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        graphic_genres = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
    else:
        graphic_genres = None

    # ==========================
    # Render template
    # ==========================
    return render(request, 'statistics.html', {
        'graphic_years': graphic_years,
        'graphic_genres': graphic_genres
    })

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Juan José Gómez'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies, 'name': 'Juan José Gómez'})

def about(request):
    return render(request, 'about.html')