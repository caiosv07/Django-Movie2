from django.shortcuts import render, redirect,get_object_or_404
from django.http.response import JsonResponse
import requests
from django.contrib import messages
from django.http import HttpResponse
from .models import Comment
from accounts.forms import ProfilePicForm, Registerform
from accounts.models import User, Favoritos
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup


TMDB_API_KEY = "5c2b64d4046292d1176bc1b248986c08"

results = []

def home(request):
    
    data = requests.get(f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=pt-br")
    top_rated = requests.get(f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=pt-br")
    filmes_populares = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=pt-br")
    series_populares = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB_API_KEY}&language=pt-br")
    top_series = requests.get(f"https://api.themoviedb.org/3/tv/top_rated?api_key={TMDB_API_KEY}&language=pt-br")
    series = requests.get(f"https://api.themoviedb.org/3/tv/on_the_air?api_key={TMDB_API_KEY}&language=pt-br")
    return render(request, 'pages/home.html', {
        "data": data.json(),
        "top_rated": top_rated.json(),
        "filmes_populares": filmes_populares.json(),
        "series":series.json(),
        "series_populares": series_populares.json(),
        "top_series":top_series.json(),  })

def search(request):

    # Get the query from the search box
    query = request.GET.get('q')
    print(query)
    # If the query is not empty
    if query:

        # Get the results from the API

        data = requests.get(f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&language=pt-br&page=1&include_adult=false&query={query}")
        print(data.json())
    else:
        return HttpResponse("Please enter a search query")
    
    

    # Render the template
    return render(request, 'pages/results.html',{
        "data": data.json(),
        "type": request.GET.get("type")
                     })
        


def view_tv_detail(request, tv_id):
    data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=pt-br")
    recommendations = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/recommendations?api_key={TMDB_API_KEY}&language=pt-br")
    query =  requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/credits?api_key={TMDB_API_KEY}&language=pt-br")
    reviews1 = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/reviews?api_key={TMDB_API_KEY}&language=en-us")
    trailer = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/videos?api_key={TMDB_API_KEY}&language=en-us")

    return render(request, "pages/tv_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "tv",
        "query": query.json(),
        "trailer": trailer.json(),
        "reviews1": reviews1.json(),
    }, )



def view_movie_detail(request, movie_id):
    query =  requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=pt-br")
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=pt-br")
    recommendations = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=pt-br")
    reviews1 = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}&language=en-us")
    trailer = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=pt-br")
    comentario = reversed(Comment.objects.filter(movie_id=movie_id))
    return render(request, "pages/movie_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "movie",
        "query": query.json(),
        "reviews1": reviews1.json(),
        "comentario": comentario,
        "trailer": trailer.json(),
    })


def comment_page(request, movie_id):
    if request.method == "POST":
        user = request.user
        comment = request.POST.get("comments")
    
    
        if not request.user.is_authenticated:
            user = User.objects.get(id=1)

        Comment(comments=comment, user=user, movie_id=movie_id).save()

        return redirect("/")

    else:
        data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
        title = data.json()["title"]

        comentario = reversed(Comment.objects.filter(movie_id=movie_id))

        return render(request, "pages/comment.html", {
            "title": title,
            "comentario": comentario,
         })


def filmes_list(request, page):
    data = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_watch_providers=8&watch_region=BR&sort_by=popularity.desc")
    action = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={28}")
    Adventure = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={12}")
    Animation = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={16}")
    Comedy = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={35}")
    Crime = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={80}")
    Documentary = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={99}")
    Drama = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={18}")
    Family = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10751}")
    Fantasy= requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres=14")
    ScienceFiction = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres=878")
    Horror = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres=27")
    Mystery = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={9648}")
    Thriller = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={53}")
    Romance = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10749}")
    War = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10752}")
    
    page_number = int(page) 
    
    if page_number:
        page_number = int(page) + 1
    context = {
        "data":data.json(),
        "action": action.json(),
        "Adventure": Adventure.json(),
        "Animation": Animation.json(),
        "Comedy": Comedy .json(),
        "Crime":  Crime.json(),
        "Documentary": Documentary.json(),
        "Drama": Drama.json(),
        "Family": Family.json(),
        "ScienceFiction": ScienceFiction.json(),
        "Fantasy": Fantasy.json(),
        "Horror": Horror.json(),
        "Mystery": Mystery.json(),
        "Thriller": Thriller.json(),
        "Romance": Romance.json(),
        "War": War.json(),
        "page_number": page_number,
    }

   

    return render(request, 'pages/list.html', context)



def tv_list(request, page):
    data = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_watch_providers=8&watch_region=BR&sort_by=popularity.desc")
    action_Adventure  = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10759}")
    Animation = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={16}")
    Comedy = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={35}")
    Crime = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={80}")
    Documentary = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={99}")
    Drama = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={18}")
    Family = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10751}")
    ScienceFiction_Fantasy = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10765}")
    Kids = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10762}")
    Mystery = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={9648}")
    Reality = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10764}")
    Romance = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10749}")
    War = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page={page}&language=pt-br&with_genres={10768}")
    
    page_number = int(page) 
    
    if page_number:
        page_number = int(page) + 1
    context = {
        "data":data.json(),
        "action_Adventure": action_Adventure.json(),
        "Animation": Animation.json(),
        "Comedy": Comedy .json(),
        "Crime":  Crime.json(),
        "Documentary": Documentary.json(),
        "Drama": Drama.json(),
        "Family": Family.json(),
        "ScienceFiction_Fantasy": ScienceFiction_Fantasy.json(),
        "Kids": Kids.json(),
        "Mystery": Mystery.json(),
        "Reality": Reality.json(),
        "Romance": Romance.json(),
        "War": War.json(),
        "page_number": page_number,
    }

   

    return render(request, 'pages/tv_list.html', context)


def person_detail(request, person_id):
    data = requests.get(f"https://api.themoviedb.org/3/person/{person_id}?api_key={TMDB_API_KEY}&language=pt-br")
    query = requests.get(f"https://api.themoviedb.org/3/person/{person_id}/combined_credits?api_key={TMDB_API_KEY}&language=pt-br")
    return render(request, "pages/person_detail.html", {
        "data": data.json(),
        "query": query.json()
    })



def reviews_page(request, movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=pt-br")
    reviews1 = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}&language=en-us")
    comentario = reversed(Comment.objects.filter(movie_id=movie_id))
    image1 = User.objects.all()
    return render(request, "pages/reviews.html", {
        "data": data.json(),
        "reviews1": reviews1.json(),
        "comentario": comentario,
        "image1":image1,
        
    })



def profile_page(request, user):
    query = User.objects.all().filter(username=request.user)
    comentario = Comment.objects.filter(user=request.user)
    return render(request, 'pages/profile_page.html',{
        "query":query,
        "comentario": comentario,
    })


def addfav(request, movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=pt-br")
    movie = data.json()["id"]
    try:
        fav = Favoritos.objects.filter(user=request.user)
    except Favoritos.DoesNotExist:
        fav = Favoritos.objects.create(user=request.user)
    try:
        if movie in Favoritos.objects.all():
            print('filme ja foi salvo')
        else:
            Favoritos.objects.create(movie_id=movie, user=request.user)
           
      
    except Favoritos.DoesNotExist:
        print('livro nao adicionado')
    return redirect('/')


def favorite_page(request, user):
        fav = Favoritos.objects.filter(user=request.user)
        image1 = User.objects.filter(username=request.user)
        movieid_list = []
        title_list = []
        poster_list = []
        if fav:
            for m in fav:
                movie= m.movie_id
                pt = []
                pt.append(movie)
                
                for n in pt:
                    data = requests.get(f"https://api.themoviedb.org/3/movie/{n}?api_key={TMDB_API_KEY}&language=pt-br")
                    title = data.json()['title']
                    poster = data.json()['poster_path']
                    movie1 = data.json()['id']
                    print(title)
                    title_list.append(title)
                    poster_list.append(poster)
                    movieid_list.append(movie1)
        else:
            return render(request, "pages/fav_page.html")
        
        return render(request, "pages/fav_page.html", {
            "poster_list":poster_list,
            "title_list":title_list,
            "data":data.json(),
            "fav": fav,
            "image1":image1,
            "pt":pt,
            "movieid_list":movieid_list,
        })

def view_movie_genro(request, genero):
    data = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page=&language=pt-br&with_genres={genero}")
    
    return render(request, "pages/movie_genro.html", {
        "data": data.json(),
        
        
    }, )

def view_tv_genro(request, genero):
    data = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&page=&language=pt-br&with_genres={genero}")
    
    return render(request, "pages/tv_genro.html", {
        "data": data.json(),
        
        
    }, )


def update_user(request):

    if request.user.is_authenticated:
        current_user =  User.objects.get(id=request.user.id)
        profile_form = ProfilePicForm(request.POST or None, request.FILES, instance=current_user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Sua foto de perfil foi mudada com sucesso')
            
    else:
        messages.success(request, 'Voçê precisa estar logado')
    return  render(request, 'pages/update_user.html', {
        "profile_form":profile_form,
        "current_user":current_user,
    })

def removefav(request, movie_id):
    data = get_object_or_404(Favoritos, movie_id=movie_id)
    data.delete()
    return redirect('favpage', user=request.user.id)