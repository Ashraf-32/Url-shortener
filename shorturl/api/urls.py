from django.urls import path
from .views import UrlAPIView, RegisterAPIView
from rest_framework.authtoken import views as authview

urlpatterns = [
    path('', UrlAPIView.as_view(), name="create-url"),
    path('register/', RegisterAPIView.as_view(), name="api-register"),
]
