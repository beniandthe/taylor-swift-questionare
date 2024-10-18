from django.urls import path
from . import views

app_name = 'questionare'
urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('question/<int:question_id>/', views.next_question, name='next_question'),
    path('results/', views.results, name='results'),  # This would handle the final results page
]
