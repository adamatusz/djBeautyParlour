import pytest

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .models import Service, Appointment
from adminsection.models import Customer

User = get_user_model()


# Create your tests here.


@pytest.mark.django_db
def test_services_view_not_logged_person(client):
    response = client.get(reverse('services'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_profile_user_view(client, user):
    client.force_login(user)
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_appointment_create_view(client, user, appointment):
    client.force_login(user)
    get_response = client.get('')
    assert get_response.status_code == 200

    url = reverse('thankyou', args=(appointment.id, ))
    post_response = client.post(url)
    assert post_response.status_code == 200
    assert Appointment.objects.get(AppointmentNumber=6000 + appointment.id)

@pytest.mark.django_db
def test_register_user_view(client, user):
    client.force_login(user)
    response = client.post(reverse('profile'))
    assert response.status_code == 200
    assert User.objects.filter(username='bleble')

@pytest.mark.django_db
def test_register_new_user_view(client, user):
    get_response = client.get(reverse('register'))
    assert get_response.status_code == 200

    count_before_create = User.objects.count()
    post_response = client.post(reverse('register'),
        {
            'username': 'bobas',
            'first_name': 'Johny',
            'last_name': 'Cash',
            'email': 'cash@onet.pl',
            'password1': 'coderslab',
            'password2': 'coderslab',
        },
        follow=True
    )

    count_after_create = User.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


