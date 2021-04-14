from django.urls import path
from .views import UrlAPIView, RegisterAPIView, LogoutAPIView, ProfileAPIView
from rest_framework.authtoken import views as authview

urlpatterns = [
    path('', UrlAPIView.as_view(), name="create-url"),
    path('register/', RegisterAPIView.as_view(), name="api-register"),
    path('login/', authview.obtain_auth_token),
    path('logout/', LogoutAPIView.as_view(), name="api-logout"),
    path('profile/', ProfileAPIView.as_view(), name="api-profile"),
]
