import pytest
import pytz
from django.db.models import Sum
from faker import Faker

from src.settings import TIME_ZONE
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .models import Customer, Service, Invoice
from parlour.models import Appointment

# from .utils import random_service

User = get_user_model()


# faker = Faker("pl_PL")
# TZ = pytz.timezone(TIME_ZONE)


# importujemy model użytkownika

# Create your tests here.

@pytest.mark.django_db
def test_random_service(random_services, service_a=None, service_b=None):
    """
    Use fixture return value in a test.
    """
    if __name__ == '__main__':
        assert random_services == service_a, service_b


@pytest.mark.django_db
def test_service_list(random_services):
    qs = Service.objects.all()
    assert len(qs) == 2


@pytest.mark.django_db
def test_service_cost(random_services):
    assert Service.objects.get(Cost=1500) == random_services[0]


@pytest.mark.django_db
def test_service_name(random_services):
    assert Service.objects.get(ServiceName__iendswith='e') == random_services[0]


@pytest.mark.django_db
def test_service_name_nail(random_services):
    assert Service.objects.get(ServiceName='Nail') == random_services[1]


@pytest.mark.django_db
def test_random_user(random_user, user_a=None):
    """
    Use fixture return value in a test.
    """
    if __name__ == '__main__':
        assert random_user == user_a


@pytest.mark.django_db
def test_customer_list(random_user):
    qs = Customer.objects.all()
    assert len(qs) == 1


@pytest.mark.django_db
def test_customer_note(random_user):
    assert Customer.objects.get(Note='śmieszny facet') == random_user


@pytest.mark.django_db
def test_customer_name(random_user):
    assert Customer.objects.get(Name__icontains='Zen') == random_user


@pytest.mark.django_db
def test_customer_name_2(random_user):
    qs = Customer.objects.filter(Name='zenek tonieten')
    assert qs.exists()


@pytest.mark.django_db
def test_home_view(admin_client):  # admin_klient przeglądarka podawany domyślnie przez pytest
    admin_client.login(username='adam',
                       password='coderslab')
    response = admin_client.get(reverse('dashboard'))
    # print(response.content)
    assert response.status_code == 200


def test_signin(client):  # klient przeglądarka podawany domyślnie przez pytest
    response = client.get(reverse('signin'))
    # print(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_acceptedappointment(admin_client):
    admin_client.login(username='adam',
                       password='coderslab')
    response = admin_client.get(reverse('acceptedappointment'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_allapointment_views_admin(admin_client):
    admin_client.login(username='adam',
                       password='coderslab')
    response = admin_client.get(reverse('allappointment'))
    # print(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_allapointment_views_no_admin(client):
    response = client.get(reverse('allappointment'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_views_admin(client, user, appointments):
    client.force_login(user)
    response = client.get(reverse('dashboard'))
    assert response.context['total_appointment'] == 10
    assert response.context['total_service'] == 2
    assert response.context['total_customer'] == 2
    assert Appointment.objects.filter(Name='Ula Brzydula').exists()
    assert Service.objects.filter(ServiceName='Lymphatic massage').exists()
    assert Service.objects.filter(ServiceName='Nail').exists()
    assert Customer.objects.filter(Email__icontains='szcz').exists()
    assert Customer.objects.filter(Gender='0').exists()
    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard_views_no_admin(client):
    response = client.get(reverse('dashboard'))
    # print(response.content)
    assert response.status_code == 302


@pytest.mark.django_db
def test_appointments_gender_choice(client, user, appointments_gender_choice):
    client.force_login(user)
    response = client.get(reverse('dashboard'))
    assert Customer.objects.filter(Gender='0').exists()
    assert Customer.objects.filter(Gender='1').exists()
    assert Customer.objects.filter(Name__icontains='Nieokreślony').exists()
    assert len(Customer.objects.filter(Gender='0')) != len(Customer.objects.filter(Gender='1'))
    assert Customer.objects.all().count() == 9
    assert response.status_code == 200


@pytest.mark.django_db
def test_sum_invoices_in_dashboard(client, user, invoice, appointments_gender_choice):
    client.force_login(user)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert Service.objects.get(Cost=1500)
    assert Customer.objects.get(Name='zenek tonieten')
    assert Customer.objects.count() == 10

@pytest.mark.django_db
def test_newappointmnet_view(client, user, random_appointment):
    client.force_login(user)
    get_response = client.get(reverse('newappointment'))
    assert get_response.status_code == 200
    assert Appointment.objects.get(Name="Teresa Nieposkromiona")


@pytest.mark.django_db
def test_view_newappointment_detail_view(client, user, random_appointment):
    client.force_login(user)
    url = reverse('viewappointment', args=(random_appointment.id,))
    post_response = client.post(url, {'Note': 'bzdzina',
                                      'Remark': 0
                                      })
    assert post_response.status_code == 200
    assert Appointment.objects.get(Note="bzdzina")
    assert Appointment.objects.get(AppointmentNumber=6000 + random_appointment.id)
    assert Appointment.objects.get(Remark=0)



@pytest.mark.django_db
def test_addservice_detail_view(client, user, random_service):
    client.force_login(user)
    get_response = client.get(reverse('addservices'))
    assert get_response.status_code == 200

    count_before_create = Service.objects.count()
    print(count_before_create)
    post_response = client.post(reverse('addservices'),
                                {'ServiceName': 'bzdzina',
                                 'Cost': 1500
                                 },
         follow=True
    )
    count_after_create = Service.objects.count()
    print(count_after_create)
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1
    assert Service.objects.get(ServiceName="bzdzina")


@pytest.mark.django_db
def test_assignservices_detail_view(client, user, random_user, invoice):
    client.force_login(user)
    url = reverse('assignservices', args=(random_user.id,))
    get_response = client.get(url)
    assert get_response.status_code == 200

    post_response = client.post(reverse('viewinvoice', args=[invoice.id]), follow=True)
    assert post_response.status_code == 200
    assert Invoice.objects.get(BillingNumber=6060 + invoice.id)


@pytest.mark.django_db
def test_invoice_view(client, user, invoice):
    client.force_login(user)
    get_response = client.get(reverse('invoices'))
    assert get_response.status_code == 200

    url = reverse('viewinvoice', args=(invoice.id, ))
    get_response_2 = client.get(url)
    assert get_response_2.status_code == 200
    assert Invoice.objects.get(BillingNumber=6060 + invoice.id)


