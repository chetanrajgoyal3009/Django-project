from django.urls import path
from . import views

app_name = 'blogbattle'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('start/', views.start, name='start'),
    path('quiz/', views.startquiz, name='quiz'),
    path('result/', views.result_view, name='submit_result'),
    path('result_page/', views.result_page_view, name='result_page'),
    path('generate-quiz/', views.generate_quiz, name='generate_quiz'),  # Note trailing slash
]
