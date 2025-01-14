from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,views,permissions
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsLibrarian, IsAdmin
from django.db import connections
from django.db import IntegrityError
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

class Member(APIView):
    #add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]
    def get(self, request):
        query = """
            select id, first_name, last_name, username, email, role, created_by  from users where role=%s and is_active=%s
        """
        data = ["MEMBER", 1]
        with connections['default'].cursor() as cursor:
            cursor.execute(query,data)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            members  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()
        return Response({"data": members}, status=status.HTTP_200_OK)

    def post(self, request ):
        username = request.data['username']
        email = request.data['email']
        password = make_password(request.data['password'])
        role = 'MEMBER'
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        is_active = 1
        created_by = request.user
        try:
            query = """
                INSERT INTO users(first_name, last_name, username, email, password, role, created_by, is_active )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = [first_name, last_name, username, email, password, role, created_by, is_active]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Username/Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Member successfully created"}, status=status.HTTP_201_CREATED)

class MemberDetails(APIView):
    #add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]
    def get(self, request, user_id):
        query = """
            select id, first_name, last_name, username, email, role, created_by, is_active  from users where role=%s and id=%s and is_active=%s
        """
        data = ["MEMBER", user_id, 1]
        with connections['default'].cursor() as cursor:
            cursor.execute(query,data)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            member  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()
        if member:
            return Response({"data": member}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "The requried Member is removed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "The requried Member is not available"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, user_id):
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        updated_by = request.user
        try:
            query = """
                UPDATE users set first_name=%s, last_name=%s, updated_by=%s where id=%s
            """
            data = [first_name, last_name, updated_by, user_id]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Member successfully updated"}, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id):
        updated_by = request.user
        query = """
           UPDATE users set is_active=0, updated_by=%s where id=%s
        """
        data = [updated_by, user_id]
        with connections['default'].cursor() as cursor:
            cursor.execute(query,data)
            cursor.close()
        return Response({"message": "Member successfully deleted"}, status=status.HTTP_200_OK)

class Remove(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, user_id):
        updated_by = request.user
        query = """
           UPDATE users set is_active=0, updated_by=%s where id=%s
        """
        data = [updated_by, user_id]
        with connections['default'].cursor() as cursor:
            cursor.execute(query,data)
            cursor.close()
        return Response({"message": "Member successfully deleted"}, status=status.HTTP_200_OK)

class Librarian(APIView):
    #add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    def post(self, request ):
        username = request.data['username']
        email = request.data['email']
        password = make_password(request.data['password'])
        role = 'LIBRARIAN'
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        is_active = 1
        created_by = request.user
        try:
            query = """
                INSERT INTO users(first_name, last_name, username, email, password, role, is_active, created_by)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = [first_name, last_name, username, email, password, role, is_active, created_by]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Username/Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Librarian successfully created"}, status=status.HTTP_201_CREATED)