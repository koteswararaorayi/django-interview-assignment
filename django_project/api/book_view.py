from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.db import connections
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status,views,permissions
from .custom_permissions import IsLibrarian
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
class Book(APIView):
    #add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]

    def post(self, request):
        title = request.data['title']
        author = request.data['author']
        publisher = request.data['publisher']
        category = request.data['category']
        created_by = request.user
        try:
            query = """
                INSERT INTO books (title, author, publisher, category, created_by)
                VALUES(%s, %s, %s, %s, %s)
            """
            data = [title, author, publisher, category, created_by]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Book title name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "book successfully added"}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        query = """
            select id, title, author, publisher, category, status from books where status=%s
        """
        data = ["AVAILABLE"]
        with connections['default'].cursor() as cursor:
            cursor.execute(query,data)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            books  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()        
        return Response({"data": books}, status=status.HTTP_200_OK)

class BookDetails(APIView):
    #add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]
    def put(self, request, book_id):
        title = request.data['title']
        author = request.data['author']
        publisher = request.data['publisher']
        category = request.data['category']
        updated_by = request.user
        try:
            query = """
                UPDATE books set title=%s, author=%s, publisher=%s, category=%s, updated_by=%s where id=%s
            """
            data = [title, author, publisher, category, updated_by, book_id]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Book title name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "book successfully updated"}, status=status.HTTP_200_OK)           

    
    def get(self, request, book_id):
        try:
            query = """
                select id, title, author, publisher, category from books where id=%s
            """
            data = [book_id]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                rows  = cursor.fetchall()
                col_names   = [names[0] for names in cursor.description]
                books  = [dict(zip(col_names, row_data)) for row_data in rows]
                cursor.close()
        except IntegrityError :
            return Response({"message": "The requried book is not available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": books}, status=status.HTTP_200_OK)

    
    def delete(self, request, book_id):
        updated_by = request.user
        query = """
           UPDATE books set status="DELETED", updated_by=%s where id=%s
        """
        data = [updated_by, book_id]
        with connections['default'].cursor() as cursor:
            cursor.execute(query,data)
            cursor.close()        
        return Response({"message": "book successfully deleted"}, status=status.HTTP_200_OK)