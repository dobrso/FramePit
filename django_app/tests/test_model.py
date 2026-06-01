import pytest
from django.contrib.auth import get_user_model

from rooms.models import Room, Tag
from users.models import Profile

User = get_user_model()

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
def another_tag(db):
    return Tag.objects.create(name='another_test_tag')

@pytest.fixture
def room(db, user, tag):
    room = Room.objects.create(name='test_room', owner=user)
    room.tags.add(tag)

    return room

class TestTag:
    def test_str(self, tag):
        assert str(tag) == 'test_tag'

class TestRoom:
    def test_auto_add_owner_to_members(self, user):
        room = Room.objects.create(name='test_room', owner=user)
        assert user in room.members.all()

    def test_new_member_join_to_room(self, room, another_user):
        room.members.add(another_user)
        assert room.members.count() == 2

    def test_room_creation(self, user, tag):
        room = Room.objects.create(name='test_room', owner=user)
        room.tags.add(tag)
        assert room.owner == user
        assert room.name == 'test_room'
        assert room.tags.count() == 1

    def test_room_creation_with_multiple_tags(self, user, tag, another_tag):
        room = Room.objects.create(name='test_room', owner=user)
        room.tags.add(tag, another_tag)
        assert room.owner == user
        assert room.name == 'test_room'
        assert room.tags.count() == 2

class TestProfile:
    def test_profile_auto_created_on_user_create(self, db):
        user = User.objects.create_user(username='test', password='')
        assert Profile.objects.filter(user=user).exists()