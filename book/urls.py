from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookListCreateView.as_view(), name="book-list-create"),
    path("<int:id>/", views.BookDetailAPIView.as_view(), name="book-detail"),
]