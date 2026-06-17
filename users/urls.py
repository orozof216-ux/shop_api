from django.urls import path
from .views import RegisterView, LoginUserView, ConfirmUserView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginUserView.as_view()),
    path('confirm/', ConfirmUserView.as_view()),
]