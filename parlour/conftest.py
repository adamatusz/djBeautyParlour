import pytest
from django.contrib.auth.models import User
from adminsection.models import Service

from .models import Appointment


@pytest.fixture
def user():
    u = User.objects.create_superuser(username='bleble', is_staff=True)
    return u


@pytest.fixture
def service():
    service_a = Service.objects.create(
        ServiceName='Permanent Makeup',
        Cost=2500
    )
    return service_a


@pytest.fixture
def appointment():
    service_a = Service.objects.create(ServiceName='Lips augmentation',
                                       Cost=2000)

    appointment = Appointment.objects.create(
                    Name='Jadwiga Król',
                    Email='król@gmail.com',
                    PhoneNumber='123098765',
                    Note='Brak słów',
                    AppointmentDate='2022-08-06',
                    AppointmentTine='12:00',
                    AppointmentNumber='2',
                    Remark=1)
    appointment.Service.add(service_a)
    return appointment

def appointment2():
    service_a = Service.objects.create(ServiceName='Lips augmentation',
                                       Cost=2500)

    appointment = Appointment.objects.create(
                    Name='Greta Garbo',
                    Email='garbo@gmail.com',
                    PhoneNumber='123098765',
                    Note='Brak słów',
                    AppointmentDate='2022-08-06',
                    AppointmentTine='12:00',
                    AppointmentNumber='2',
                    Remark=1)
    appointment.Service.add(service_a)
    return appointment2
