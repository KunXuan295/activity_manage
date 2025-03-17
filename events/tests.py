from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Event, Comment, Participation
from datetime import datetime, timedelta

class EventTests(TestCase):
    def setUp(self):

        self.user = get_user_model().objects.create_user(
    username='testuser',
    password='testpass123'
    )

        self.event = Event.objects.create(
    title='Test Event',
    description='Test Description',
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=2),
    location='Test Location',
    organizer=self.user
    )

def test_event_creation(self):

    self.assertEqual(self.event.title, 'Test Event')
    self.assertEqual(self.event.organizer, self.user)

def test_event_list_view(self):

    self.client.login(username='testuser', password='testpass123')
    response = self.client.get(reverse('events_list'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Test Event')

def test_event_detail_view(self):

    self.client.login(username='testuser', password='testpass123')
    response = self.client.get(reverse('event_details', args=[self.event.id]))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Test Event')

def test_event_participation(self):

    self.client.login(username='testuser', password='testpass123')
    response = self.client.post(reverse('join_event', args=[self.event.id]))
    self.assertEqual(response.status_code, 200)
    self.assertTrue(Participation.objects.filter(user=self.user, event=self.event).exists())