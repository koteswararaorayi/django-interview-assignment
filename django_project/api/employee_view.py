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
from .models import Employee
from .serializers import EmployeeSerializer
from django.http import JsonResponse

class EmployeeSql(APIView):
    #add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated, IsLibrarian]
    def post(self, request ):
        name = request.data['name']
        email = request.data['email']
        phone_no = request.data['phone_no']
        gender = request.data['gender']
        address = request.data['address']
        try:
            query = """
                INSERT INTO employee (name, email, phone_no, gender, address)
                VALUES(%s, %s, %s, %s, %s)
            """
            data = [name, email, phone_no, gender, address]
            with connections['default'].cursor() as cursor:
                cursor.execute(query,data)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Employee successfully Registered"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        query = """
            select * from employee
        """
        with connections['default'].cursor() as cursor:
            cursor.execute(query)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            member  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()
        if member:
            return Response({"data": member}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "The requried Member is removed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "The requried Employee is not available"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        name = request.data['name']
        email = request.data['email']
        phone_no = request.data['phone_no']
        gender = request.data['gender']
        address = request.data['address']
        try:
            query = """
                UPDATE employee set name=%s, phone_no=%s, gender=%s, address=%s  where email=%s
            """
            data = [name, phone_no, gender, address, email]
            with connections['default'].cursor() as cursor:
                rows = cursor.execute(query,data)
                cursor.close()
            if rows:
                return Response({"message": "Employee Details Successfully Updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Employee with this eamil does not exists"}, status=status.HTTP_400_BAD_REQUEST)             
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        email = request.data['email']
        query = """
           delete from employee where email=%s
        """
        data = [email]
        with connections['default'].cursor() as cursor:
            rows = cursor.execute(query,data)
            cursor.close()
        if rows:
            return Response({"message": "Employee Details Successfully deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Employee with this eamil does not exists"}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeModel(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        email= request.data.get('email')
        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            return Response({"message": "Employee with this eamil does not exists"},status=status.HTTP_400_BAD_REQUEST)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        email= request.data.get('email')
        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            return Response({"message": "Employee with this eamil does not exists"},status=status.HTTP_400_BAD_REQUEST)
        employee.delete()
        return Response({"message": "Employee deleted!"},status=status.HTTP_200_OK)