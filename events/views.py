from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User,Event,Comment,Participation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.timezone import now
import json


# Create your views here.
def home(request):
    return render(request, 'events/home.html')

# login view
from django.contrib.auth import get_user_model

User = get_user_model()  # This ensures that the custom User model is used

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if isinstance(user, User):  # Make sure the user is a customized User
            login(request, user)
            if user.role == "admin":
                return redirect("admin_home")
            return redirect("user_home")
        else:
            return render(request, "events/login.html", {"error": "Incorrect user name or password"})

    return render(request, "events/login.html")

# Register View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            return render(request, "events/register.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, password=password, role=role)
        user.save()

        return redirect("login")

    return render(request, "events/register.html")

# User homepage
@login_required
def user_home(request):
    return render(request, "events/user_home.html", {"user": request.user})

# Administrator's Home Page
@login_required
def admin_home(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.role == 'admin'):
        return redirect('user_home')  # If you don't have permission, redirect to normal user homepage
    
    # Get the latest campaigns, in descending order of when they were created
    latest_event = Event.objects.all().order_by('-created_at').first()
    
    return render(request, "events/admin_home.html", {
        "user": request.user,        # Currently logged in user
        "latest_event": latest_event # Latest Activities
    })
    

# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")


# Event Listings
def events_list_view(request):
    # Get search parameters
    search_term = request.GET.get('search_term', '')  # Defaults to the empty string
    
    # Filter activities based on search criteria
    events = Event.objects.filter(title__icontains=search_term, is_approved=True)
    
    # Renders the page and returns
    return render(request, 'events/events_list.html', {
        'events': events,  
        'search_term': search_term  
    })

def event_details_view(request, event_id):
    event = get_object_or_404(Event.objects.select_related('organizer').prefetch_related('comments'), id=event_id)
    return render(request, 'events/event_details.html', {'event': event})

@csrf_exempt
@login_required
def add_comment(request, event_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  
            content = data.get('content')

            if content:
                event = Event.objects.get(id=event_id)
                comment = Comment.objects.create(
                    event=event,
                    user=request.user,
                    content=content
                )
                return JsonResponse({
                    'success': True,
                    'username': request.user.username,
                    'content': content,
                    'created_at': comment.created_at.strftime("%d/%m/%Y %H:%M")  
                })
            else:
                return JsonResponse({'success': False, 'error': 'Comment content is empty.'})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def join_event(request, event_id):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You need to log in first."}, status=403)

    event = get_object_or_404(Event, id=event_id)

    if now() > event.end_time:
        return JsonResponse({"success": False, "message": "This event has expired."}, status=400)

    if Participation.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({"success": False, "message": "You have already joined this event."}, status=400)

    Participation.objects.create(user=request.user, event=event)

    return JsonResponse({"success": True})

@login_required
def my_participations(request):
    participations = Participation.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/my_participations.html', {'participations': participations})

@login_required
def add_event(request):
    if request.method == 'POST':
        try:
            # Getting data from a form
            title = request.POST.get('title')
            description = request.POST.get('description')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            location = request.POST.get('location')
            max_participants = request.POST.get('max_participants')

            # Founding activities
            event = Event.objects.create(
                title=title,
                description=description,
                organizer=request.user,
                start_time=start_time,
                end_time=end_time,
                location=location,
                max_participants=max_participants if max_participants else None
            )
            return JsonResponse({'success': True, 'message': 'Event created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return render(request, 'events/add_events.html')

def admin_event_list(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.role == 'admin'):
        return redirect('user_home')  # If you don't have permission, redirect to normal user homepage
  
    search_term = request.GET.get('search_term', '')  
    
    # Only approved activities are displayed
    events = Event.objects.filter(title__icontains=search_term, is_approved=True)

    # Renders the page and returns
    return render(request, 'events/admin_event_list.html', {
        'events': events,  
        'search_term': search_term  
    })

def admin_event_details_view(request, event_id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.role == 'admin'):
        return redirect('user_home')  # If you don't have permission, redirect to normal user homepage
    
    event = get_object_or_404(
        Event.objects.select_related('organizer').prefetch_related('comments'), 
        id=event_id
    )
    return render(request, 'events/admin_event_details.html', {'event': event})

def reject_event_view(request, event_id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.role == 'admin'):
        return redirect('user_home')  # If you don't have permission, redirect to normal user homepage
    
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        event.delete()  # Delete Activity
        return JsonResponse({"message": "Event rejected"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render
from events.models import Event
