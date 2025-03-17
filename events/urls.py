from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('user_home/', views.user_home, name='user_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('logout/', views.logout_view, name='logout'),
    path('events_list/', views.events_list_view, name='events_list'),
    path('event_details/<int:event_id>/', views.event_details_view, name='event_details'),
    path('event/<int:event_id>/add_comment/', views.add_comment, name='add_comment'),
    path('event/<int:event_id>/join/', views.join_event, name='join_event'),
    path('my_participations/', views.my_participations, name='my_participations'),
    path('add_event/', views.add_event, name='add_event'),
    path('admin_home/events/', views.admin_event_list, name='admin_event_list'),
    path('admin_home/event/<int:event_id>/', views.admin_event_details_view, name='admin_event_details'),
    path('admin_home/event/<int:event_id>/reject/', views.reject_event_view, name='reject_event'),

]
