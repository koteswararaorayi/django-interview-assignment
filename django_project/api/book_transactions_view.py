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

class TransactionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(request.user.id)
        query = """
            select id, title, author, publisher, category, status from books where status!=%s
        """
        data = ["DELETED"]
        with connections['default'].cursor() as cursor:
            cursor.execute(query,data)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            books  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()        
        return Response({"data": books}, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data['title']
        book_type = request.data['type']
        member = request.user
        try:
            query = """
                INSERT INTO transactions (title, type, member_name)
                VALUES(%s, %s, %s)
            """
            data = [title, book_type, member]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "book successfully borrowed/returned"}, status=status.HTTP_201_CREATED)