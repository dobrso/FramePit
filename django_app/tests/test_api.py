import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from rooms.models import Tag, Room

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='test_user', email='test_email@example.com', password='test_password')

@pytest.fixture
def another_user(db):
    return User.objects.create_user(username='another_test_user', email='another_test_email@example.com', password='another_test_password')

@pytest.fixture
def tag(db):
    return Tag.objects.create(name='test_tag')

@pytest.fixture
def room(db, user, another_user, tag):
    room = Room.objects.create(name='test_room', owner=user)
    room.tags.add(tag)
    room.members.add(user, another_user)

    return room

class TestRoomAPI:
    def test_rooms_api_returns_list(self, api_client, room):
        url = reverse('rooms:api_room_list')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['name'] == room.name
        assert data[0]['owner']['username'] == room.owner.username
        assert data[0]['members_count'] == room.members.count()

    def test_rooms_retrieve_api_returns_room_object(self, api_client, room):
        url = reverse('rooms:api_room_detail', args=[room.pk])
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == room.name
        assert data['owner']['username'] == room.owner.username
        assert len(data['members']) == room.members.count()
        assert len(data['tags']) == room.tags.count()
        assert data['members'][1]['username'] == room.members.all()[1].username

class TestProfileAPI:
    def test_profile_retrieve_api_returns_current_user(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('users:api_me')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['user']['username'] == user.username
        assert 'description' in data

    def test_profile_retrieve_api_returns_forbidden(self, api_client):
        url = reverse('users:api_me')
        response = api_client.get(url)
        assert response.status_code == 403