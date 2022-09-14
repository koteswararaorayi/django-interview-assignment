from django.urls import path, include
from . import book_view, book_transactions_view, member_view, employee_view

app_name = "api"

urlpatterns = [
    path('book', book_view.Book.as_view()),
    path('book/<int:book_id>', book_view.BookDetails.as_view(), name='book'),
    path('books', book_transactions_view.Transaction.as_view()),
    path('transactions', book_transactions_view.Transaction.as_view()),
    path('member', member_view.Member.as_view()),
    path('member/<int:user_id>', member_view.MemberDetails.as_view()),
    path('delete/<int:user_id>', member_view.Remove.as_view()),
    path('librarian', member_view.Librarian.as_view()),
    path('employee', employee_view.EmployeeSql.as_view()),
    path('employee_reg', employee_view.EmployeeModel.as_view()),
]