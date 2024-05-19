import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View, generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from .models import *
from .form import *
from account.models import *


# Create your views here.

def get_items():
    items = []
    for i, movie in enumerate(Movie.objects.all()):
        item = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'trailer': movie.trailer,
            'poster': movie.poster,
            'banner' : movie.banner,
            'age': movie.age,
            'rating': movie.rating,
            'status': movie.status,
            'released_date': movie.released_date,
            'director': movie.director,
            'actor' : movie.actor,
            'language' : movie.language,
            'country' : movie.country,
            'duration' : movie.duration,
            'genre': movie.genre
        }
        # print(item)
        items.append(item)
    return items



class MovieView(View):
    template_name = "film.html"
    Model = Movie

    def list_movie_now(self):
        today = datetime.date.today()
        movies = []
        for i, movie in enumerate(Movie.objects.all()):
            if movie.released_date == today:
                movie.status = 'now'
                item = {
                    'id': movie.id,
                    'title': movie.title,
                    'description': movie.description,
                    'trailer': movie.trailer,
                    'poster': movie.poster,
                    'banner': movie.banner,
                    'age': movie.age,
                    'rating': movie.rating,
                    'status': movie.status,
                    'released_date': movie.released_date,
                    'director': movie.director,
                    'actor': movie.actor,
                    'language': movie.language,
                    'country': movie.country,
                    'duration': movie.duration,
                    'genre': movie.genre
                }
                movies.append(item)
        return movies

    def list_movie_soon(self):
        today = datetime.date.today()
        movies = []
        for i, movie in enumerate(Movie.objects.all()):
            if movie.released_date > today:
                movie.status = 'soon'
                item = {
                    'id': movie.id,
                    'title': movie.title,
                    'description': movie.description,
                    'trailer': movie.trailer,
                    'poster': movie.poster,
                    'banner': movie.banner,
                    'age': movie.age,
                    'rating': movie.rating,
                    'status': movie.status,
                    'released_date': movie.released_date,
                    'director': movie.director,
                    'actor': movie.actor,
                    'language': movie.language,
                    'country': movie.country,
                    'duration': movie.duration,
                    'genre': movie.genre
                }
                movies.append(item)
        return movies

    def get(self, request):
        context = {
            'items': get_items(),
            'movies_now' : self.list_movie_now(),
            'movies_soon' : self.list_movie_soon(),
            'current_tab': 'film'
        }

        return TemplateResponse(request, self.template_name, context)


@method_decorator([
    login_required(login_url='/login'),
    permission_required('movie.add_movie', raise_exception=True),
], name='dispatch')
class AddMovieView(View):
    template_name = 'add_film.html'
    Model = Movie

    def get(self, request):
        context = {
            'form': MovieForm(),
            'current_tab': 'add_film'
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['add_movie'] = 'Add movie Successfully'
            messages.success(request, 'Movie added successfully')
        else:
            request.session['add_movie'] = 'Movie with this Title already exists'
            messages.error(request, 'Failed to add movie. Please check the form.')
        return HttpResponseRedirect("/film")
    


@login_required(login_url='/login')
@permission_required('movie.change_movie', raise_exception=True)
def update_film(request, id):
    movie = Movie.objects.get(id=id)
    form = MovieForm(instance=movie)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            request.session['update_movie'] = 'Update movie Successfully'
            messages.success(request, 'Movie updated successfully')
            return HttpResponseRedirect('/film')
        else :
            request.session['update_movie'] = 'Update movie fail'
            print(form.errors)
            messages.success(request, 'Movie updated fail')
    return render(request, "update_film.html", {"form": form})


@login_required(login_url='/login')
@permission_required('movie.delete_movie', raise_exception=True)
def delete_film(request, id):
    movie = Movie.objects.get(id=id)
    movie.delete()
    request.session['delete_movie'] = 'Delete movie Successfully'
    return HttpResponseRedirect('/film')


def list_review():
    reviews = []
    for i, review in enumerate(CustomerRating.objects.all()):
        item = {
            'user' : review.user.username if review.user is not None else 'loi',
            'movie' : review.movie,
            'review' : review.review,
            'rating' : review.rating,
            'create_at' : review.create_at
        }
        # print(item)
        reviews.append(item)
    return reviews


def movie_rating(id):
    movie = Movie.objects.get(id=id)
    list_reviews = list_review()
    result = []
    for review in list_reviews:
        if review.get('movie') == movie:
            # print(review['rating'])
            movie.rating += review['rating']
            result.append(review)
    if len(result) != 0:
        movie.rating /= len(result)
        movie.save()
        # print(movie.rating)
    # print(result)
    return movie.rating


def detail_movie(request, id):
    try:
        movie = Movie.objects.get(id=id)
        list_reviews = list_review()
        result = []
        for review in list_reviews:
            if review.get('movie') == movie:
                result.append(review)
        # print(result)

    except Movie.DoesNotExist:
        raise HttpResponseRedirect('/film')

    return render(request, 'movie_detail.html',
                  {'movie': movie, 'reviews': result, 'rating' : movie.rating})


@login_required(login_url='/login')
def review_rating(request, id):
    movie = Movie.objects.get(id=id)
    id = movie.id
    user = request.user
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            # print(user.username, User.objects.filter(username=user.username))
            rate.user = User.objects.get(username=user.username)
            rate.movie = movie
            rate.save()
            movie.rating = movie_rating(id)
            movie.save()
            return HttpResponseRedirect('/film/' + str(id))
        else:
            form = ReviewForm()

    context = {
        "form" : form,
        "movie" : movie,
        'message' : 'Rate movie successfully'
    }

    return render(request, "review_rating.html", context)

