from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

# Type of activity
class Event(models.Model):
    title = models.CharField(max_length=255)  # Activity Title
    description = models.TextField()  # Description of activities
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')  # organisers
    start_time = models.DateTimeField()  # Event start time
    end_time = models.DateTimeField()  # Activity end time
    location = models.CharField(max_length=255)  # Event Location
    max_participants = models.PositiveIntegerField(null=True, blank=True)  # Maximum number of participants (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # Creation time
    is_approved = models.BooleanField(default=True)  # Whether it has been reviewed or not, default has been reviewed

    def __str__(self):
        return self.title

# Activity Participation Record
class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')  # participant
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')  # Participation in activities
    joined_at = models.DateTimeField(auto_now_add=True)  # Participation time

    class Meta:
        unique_together = ('user', 'event')  # Preventing Duplicate Enrollment

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"

# Activity comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # user of computer software
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')  # Activities commented on
    content = models.TextField()  # Comments
    created_at = models.DateTimeField(auto_now_add=True)  # Comment Time

    def __str__(self):
        return f"{self.user.username} on {self.event.title}: {self.content[:30]}"  # Display only the first 30 characters

