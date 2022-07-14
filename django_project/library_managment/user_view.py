from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,views,permissions
from rest_framework.permissions import IsAuthenticated
from django.db import connections
from django.db import IntegrityError
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

class Admin(APIView):
    #add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]
    def post(self, request ):
        username = request.data['username']
        email = request.data['email']
        password = make_password(request.data['password'])
        role = 'ADMIN'
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        is_active = 1
        try:
            query = """
                INSERT INTO users(first_name, last_name, username, email, password, role, is_active )
                VALUES(%s, %s, %s, %s, %s, %s, %s)
            """
            data = [first_name, last_name, username, email, password, role, is_active]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Admin successfully created"}, status=status.HTTP_201_CREATED)