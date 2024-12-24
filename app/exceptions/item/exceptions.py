from app.exceptions.base import BaseHTTPException
from fastapi import status

class ExcItemNotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Задача не существует"