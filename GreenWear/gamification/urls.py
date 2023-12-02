from django.urls import path
from . import views

urlpatterns = [
    path('quiz<int:quiz_id>/', views.quiz, name='quiz'),
]