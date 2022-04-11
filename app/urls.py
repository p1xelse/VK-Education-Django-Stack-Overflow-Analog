from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="home"),
    path('question/<int:i>/', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag>', views.questions_with_tag, name='tag'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
]
