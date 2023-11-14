
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path("search/", views.search, name="search"),
    path("tv/<int:tv_id>/", views.view_tv_detail, name="tvdetail"),
    path("movie/<int:movie_id>/", views.view_movie_detail, name="moviedetail"),
    path("person/<int:person_id>/", views.person_detail, name="person-id"),
    path("movie/<int:movie_id>/comments/", views.comment_page, name="comments"),
    path('movie/lista/<int:page>/', views.filmes_list, name='movielist'),
    path('tv/lista/<int:page>/', views.tv_list, name='tvlist'),
    path("reviews/<int:movie_id>/", views.reviews_page, name="reviews-page"),
    path("user/<int:user>/", views.profile_page, name="profile-page"),
    path('addfav/<int:movie_id>', views.addfav, name='addfav'),
    path("user/<int:user>/fav/", views.favorite_page, name="favpage"),
    path("movie/genero/<int:genero>/", views.view_movie_genro, name="moviegenro"),
    path("tv/genero/<int:genero>/", views.view_tv_genro, name="tvgenro"),
    path('update_user/', views.update_user, name='update_user'),
    path('deletefav/<int:movie_id>', views.removefav, name='deletefav'),
]