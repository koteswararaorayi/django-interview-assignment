from django.urls import path, include
from . import book_view, book_transactions_view

app_name = "api"

urlpatterns = [
    path('book', book_view.Book.as_view()),
    path('book/<int:book_id>/', book_view.Book.as_view()),
    path('books', book_transactions_view.TransactionsView.as_view()),
    path('transactions', book_transactions_view.TransactionsView.as_view()),
]