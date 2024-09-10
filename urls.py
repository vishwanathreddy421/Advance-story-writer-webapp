# story_writer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('templates/signup.html/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('stories.html', views.stories, name='stories'),
    path('create.html/', views.story_create, name='create'),
    path('create.html/', views.story_create, name='create_story'),
    path('delete_story.html/<int:story_id>/', views.delete_story, name='delete_story'),
    path('edit_story.html/<int:story_id>/', views.edit_story, name='edit_story'),
    path('text-to-speech/<int:story_id>/', views.text_to_speech, name='text_to_speech'),
    path('speech-to-text/', views.speech_to_text, name='speech_to_text'),
    path('save/<int:story_id>/', views.save_story, name='save_story'),
    path('convert-to-pdf/<int:story_id>/', views.convert_to_pdf, name='convert_to_pdf'),
    path('search/', views.search_stories, name='search_stories'),

    path('story/<int:story_id>/add_feedback/', views.add_feedback, name='add_feedback'),
] 
