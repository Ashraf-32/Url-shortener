from django.urls import path
from .views import UrlAPIView

urlpatterns = [
    path('', UrlAPIView.as_view(), name="create-url")
]
