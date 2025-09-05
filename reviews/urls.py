# reviews/urls.py - Correct Example
from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
)
from . import views


urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/review/add/', ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
]