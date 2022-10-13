import random

import pytest
from django.contrib.auth.models import User

from adminsection.models import Customer, Service, Invoice
from parlour.models import Appointment
from django.db.models import Sum

@pytest.fixture
def user():
    u = User.objects.create_superuser(username='bleble', is_staff=True)
    return u

@pytest.fixture
def random_user():
    user_a = Customer.objects.create(
        Name='zenek tonieten',
        Email='tonieten@gmail.com',
        PhoneNumber='012345678',
        Gender='0',
        Note='śmieszny facet'
    )
    return user_a

@pytest.fixture
def random_service():
    service_a = Service.objects.create(
        ServiceName='Permanent Makeup',
        Cost=2500
    )
    return service_a

@pytest.fixture
def random_services():
    service_a = Service.objects.create(
        ServiceName='Lymphatic massage',
        Cost=1500
    )
    service_b = Service.objects.create(
        ServiceName='Nail',
        Cost=150
    )
    lst = [service_a, service_b]
    return lst


@pytest.fixture
def random_appointment():
    service_a = Service.objects.create(ServiceName='Lips injection',
                                       Cost=1400)
    appointment_a = Appointment.objects.create(
                        Name="Teresa Nieposkromiona",
                        Email='nieposkromiona@gmail.com',
                        PhoneNumber='321654321',
                        AppointmentDate='2022-08-09',
                        AppointmentTine='12:00',
                        Note='ala ma tako',
                        Remark=1
                        )
    appointment_a.Service.add(service_a)
    return appointment_a


@pytest.fixture
def appointments(user, random_user, random_services):

    customer_a = Customer.objects.create(Name="Wieńczyslaw Nieszczególny",
                                         Email='nieszczegolny@gmail.com',
                                         PhoneNumber='202020202')
    lst = []
    for x in range(10):

        appointment_a = Appointment.objects.create(
                            user=user,
                            Name='Ula Brzydula',
                            Email='brzydula@gmail.com',
                            PhoneNumber='321654321',
                            AppointmentDate='2022-08-08',
                            AppointmentTine='14:00')
        appointment_a.Service.add(random_services[1])
        item = appointment_a.save()
        lst.append(item)

    return lst, customer_a


@pytest.fixture
def appointments_gender_choice(user):
        GENDER_CHOICES = (
            ('0', 'Male'),
            ('1', 'Female'),
        )
        lst = []
        for x in range(9):
            gender_choice = Customer.objects.create(
                            Name="Jan Maria Nieokreślony",
                            Gender=random.choice(GENDER_CHOICES)[0]
             )
            gender_choice.save()
            lst.append(gender_choice)
        return lst


@pytest.fixture
def invoice(user, random_user, random_services):
    invoice_a = Invoice.objects.create(Customer=random_user,
                                       BillingNumber=11)
    invoice_a.Categories.add(random_services[0])
    return invoice_a
