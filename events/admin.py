from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Event, User, Comment, Participation

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Participation)
