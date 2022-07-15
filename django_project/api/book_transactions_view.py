from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.db import connections
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status,views,permissions
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

class Transaction(APIView):
    permission_classes = [permissions.IsAuthenticated]
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

    def post(self, request):
        book_id = request.data['book_id']
        book_status = request.data['book_status']
        member = request.user
        if book_status == "borrowed":
            book_status = "BORROWED"
        if book_status == "returned":
            book_status = "AVAILABLE"
        try:
            query = """
                INSERT INTO transactions (book_id, book_status, member)
                VALUES(%s, %s, %s)
            """
            data = [book_id, book_status, member]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                query = """
                    UPDATE books set status=%s where id=%s
                """
                data = [book_status, book_id]
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "book successfully borrowed/returned"}, status=status.HTTP_201_CREATED)