# File: core/utils.py
from rest_framework.response import Response
from rest_framework import status

def simple_response(data=None, message='', code=status.HTTP_200_OK):
    return Response({'message': message, 'data': data}, status=code)
