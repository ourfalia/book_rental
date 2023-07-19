from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('book_list', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/reserve/', views.reserve_book, name='reserve_book'),
]
