# story_writer/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import speech_recognition as sr
from gtts import gTTS
import io
import pdfkit
from story_writer.models import Story, Feedback
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import StoryForm, FeedbackForm 
@login_required
def stories(request):
    stories = Story.objects.all()
    return render(request, 'stories.html', {'stories': stories})
@login_required
def search_stories(request):
    query = request.GET.get('query')
    if query:
        stories = Story.objects.filter(title__icontains=query)
    else:
        stories = Story.objects.all()
    return render(request, 'stories.html', {'stories': stories})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired URL name
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Replace 'login' with your login URL name
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from story_writer.models import Story

@login_required
def edit_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Update the story object
        story.title = title
        story.content = content
        story.save()
        return redirect('home')  # Redirect to home page after saving
    
    return render(request, 'edit_story.html', {'story': story})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from story_writer.models import Story

@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    
    if request.method == 'POST':
        story.delete()
        return redirect('home')  # Redirect to home page after deletion
    
    return render(request, 'delete_story.html', {'story': story})

@login_required
def home(request):
    stories = Story.objects.filter(author=request.user)
    return render(request, 'home.html', {'stories': stories})

@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)  # Include request.FILES for handling image data
        if form.is_valid():
            # Process form data
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']  # Retrieve image data from form
            # Create new Story object but don't save it yet
            new_story = form.save(commit=False)
            new_story.author = request.user
            # Assign the image field to the Story instance
            new_story.image = image
            new_story.save()  # Now save the Story object with image
            # Redirect to a success page or any other action
            return redirect('create_story')  # Redirect to home page after saving
    else:
        form = StoryForm()  # If not POST, create a new empty form instance

    return render(request, 'story_create.html', {'form': form})

@login_required
def text_to_speech(request, story_id):
    story = Story.objects.get(id=story_id)
    tts = gTTS(story.content, lang='en')
    speech_io = io.BytesIO()
    tts.write_to_fp(speech_io)
    speech_io.seek(0)
    return HttpResponse(speech_io, content_type='audio/mpeg')

@login_required
def speech_to_text(request):
    if request.method == 'POST':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = r.record(source, duration=5)  # Adjust duration as needed
            text = r.recognize_google(audio_data)
            return render(request, 'speech_to_text.html', {'text': text})
    return render(request, 'speech_to_text.html')

@login_required
def save_story(request, story_id):
    story = Story.objects.get(id=story_id)
    # Logic to save the story
    return HttpResponse("Story saved successfully!")

@login_required
def convert_to_pdf(request, story_id):
    story = Story.objects.get(id=story_id)
    pdf_content = f"<h1>{story.title}</h1><p>Author: {story.author.username}</p><p>{story.content}</p>"
    pdf = pdfkit.from_string(pdf_content, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="story.pdf"'
    return response
@login_required
def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    feedbacks = story.feedback_set.all()
    return render(request, 'story_detail.html', {'story': story, 'feedbacks': feedbacks})
@login_required
def add_feedback(request, story_id):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            author = request.user
            story = get_object_or_404(Story, id=story_id)
            Feedback.objects.create(story=story, text=text, author=author)
            return redirect('story', story_id=story_id)
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})


