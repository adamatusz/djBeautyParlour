from django.shortcuts import (render,
                              get_object_or_404,
                              redirect)
from adminsection.forms import (LoginForm,
                                AddServiceForm,
                                AddCustomerForm,
                                AppointmentUpdateForm)
from adminsection.models import (Service,
                                 Customer,
                                 Invoice)
from parlour.models import Appointment
from django.contrib import auth
from django.urls import reverse
from django.db.models import Sum
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

# Create your views here.


def signin(request):
    """
        LogIn page for Admin/Staff
    """
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('dashboard')

    else:

        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return redirect('dashboard')

    return render(request, 'adminsection/signin.html', {'form': form})


@staff_member_required
def dashboard(request):
    """
        Adminsection Dashboard.
    """
    total_appointment = Appointment.objects.count()
    total_new_appointment = Appointment.objects.filter(Remark='').count()
    total_accepted_appointment = Appointment.objects.filter(Remark=1).count()
    total_Rejected_appointment = Appointment.objects.filter(Remark=0).count()
    total_service = Service.objects.count()
    total_customer = Customer.objects.count()
    total_sales = Invoice.objects.values('Categories__Cost').aggregate(Sum('Categories__Cost'))
    today_sales = Invoice.objects.filter(Date__date=date.today()).aggregate(Sum('Categories__Cost'))
    yesterday_sales = Invoice.objects.filter(Date__date=date.today() - timedelta(days=1)).aggregate(Sum(
                                                                                                    'Categories__Cost'))
    last_seven_days_sales = Invoice.objects.filter(Date__gte=date.today() - timedelta(days=7)).aggregate(Sum(
                                                                                                    'Categories__Cost'))

    return render(request, 'adminsection/dashboard.html',
                  context={'total_appointment': total_appointment,
                           'total_new_appointment': total_new_appointment,
                           'total_accepted_appointment': total_accepted_appointment,
                           'total_Rejected_appointment': total_Rejected_appointment,
                           'total_service': total_service,
                           'total_customer': total_customer,
                           'total_sales': total_sales,
                           'today_sales': today_sales,
                           'yesterday_sales': yesterday_sales,
                           'last_seven_days_sales': last_seven_days_sales
                           })


@staff_member_required
def addservice(request):
    """
        Admin can add Service and Price.
    """
    form = AddServiceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manageservices')

    return render(request, 'adminsection/add_services.html', context={'form': form})


@staff_member_required
def manageservices(request):
    """
        Admin can check the service list.
    """
    Services = Service.objects.order_by('-TimeStamp')

    return render(request, 'adminsection/manage_services.html', context={'Services': Services})


@staff_member_required
def updateservice(request, id):
    """
        Admin can update any service.
    """
    service = get_object_or_404(Service, id=id)
    form = AddServiceForm(request.POST or None, instance=service)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manageservices')

    return render(request, 'adminsection/edit_services.html', context={'form': form})


@staff_member_required
def addcustomer(request):
    """
        Admin can add customer details.
    """
    form = AddCustomerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('customerlist')

    return render(request, 'adminsection/add_customer.html', context={'form': form})


@staff_member_required
def customerlist(request):
    """
        Customer list.
    """
    CustomerList = Customer.objects.order_by('-CreateDate')

    return render(request, 'adminsection/customer_list.html', context={'CustomerList': CustomerList})


@staff_member_required
def editcustomer(request, id):
    """
        Edit customer details.
    """
    customer = get_object_or_404(Customer, id=id)
    form = AddCustomerForm(request.POST or None, instance=customer)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('customerlist')

    return render(request, 'adminsection/edit_customer_detailed.html', context={'form': form})


@staff_member_required
def assignservices(request, id):
    """
       Can assign services for  Customer.
    """

    customer = get_object_or_404(Customer, id=id)
    Services = Service.objects.order_by('-TimeStamp')

    if request.method == 'POST':
        serviceid = request.POST.getlist('serviceid')

        instance = Invoice()
        instance.Customer = customer
        instance.save()
        for obj in serviceid:
            instance.Categories.add(obj)

        return redirect(reverse("viewinvoice", kwargs={'id': instance.id}))

    return render(request, 'adminsection/add_customer_services.html',
                  context={'Services': Services,
                           'customer': customer})


@staff_member_required
def viewinvoice(request, id):
    """
        view Invoice .
    """

    invoice = get_object_or_404(Invoice, id=id)
    total = Invoice.objects.filter(id=id).aggregate(Sum('Categories__Cost'))

    return render(request, 'adminsection/view_invoice.html', context={'invoice': invoice,
                                                                      'total': total})


@staff_member_required
def allappointment(request):

    """
        Appointment Lists.
    """
    Appointments = Appointment.objects.order_by('-ApplyDate')
    return render(request, 'adminsection/all_appointment.html', context={'Appointments': Appointments})


@staff_member_required
def viewappointment(request, id):
    """
        View appointment.
    """

    appointment = get_object_or_404(Appointment, id=id)
    form = AppointmentUpdateForm(request.POST or None, instance=appointment)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # return redirect('manageservices')
    return render(request, 'adminsection/view_appointment.html', context={'Appointment': appointment,
                                                                          'form': form})


@staff_member_required
def newappointment(request):
    """
        New appointments list.
    """
    newappointments = Appointment.objects.filter(Remark='')
    return render(request, 'adminsection/new_appointment.html',
                  context={'newappoinments': newappointments})


@staff_member_required
def acceptedappointment(request):
    """
        Accepted appointments list.
    """
    acceptedappointments = Appointment.objects.filter(Remark=1)
    return render(request, 'adminsection/accepted_appointment.html',
                  context={'acceptedappointments': acceptedappointments})


@staff_member_required
def rejectedappointment(request):
    """
        Rejected appointments.
    """
    rejectedtedappointments = Appointment.objects.filter(Remark=0)
    return render(request, 'adminsection/rejected_appointment.html',
                  context={'rejectedtedappointments': rejectedtedappointments})


@staff_member_required
def invoices(request):
    """
        Invoice lists.
    """
    invoices = Invoice.objects.order_by('-id')
    return render(request, 'adminsection/invoices.html', context={'invoices': invoices})


@staff_member_required
def searchappointment(request):
    appointment_list = ''
    query = request.GET.get('searchdata')
    if query:
        appointment_list = Appointment.objects.all()
        appointment_list = appointment_list.filter(
            Q(AppointmentNumber__iexact=query) |
            Q(Name__icontains=query) |
            Q(Email__iexact=query)
        ).distinct()
    return render(request, 'adminsection/search_appointment.html',
                  context={'appointment_list': appointment_list,
                           'query': query})


@staff_member_required
def searchinvoices(request):
    invoices_list = ''
    query = request.GET.get('searchdata')
    if query:
        invoices_list = Invoice.objects.all()
        invoices_list = invoices_list.filter(Customer__Name__icontains=query)
    try:
        invoices_list2 = Invoice.objects.filter(BillingNumber=query)
        invoices_list |= invoices_list2
    except:
        pass
    return render(request, 'adminsection/search_invoices.html',
                  context={
                        'invoices_list': invoices_list,
                        'query': query
                  })


@staff_member_required
def bwdatesreportsds(request):
    invoice_list = ''
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:

        invoice_list = Invoice.objects.all()

        invoice_list = invoice_list.filter(
            Q(Date__gte=from_date),
            Q(Date__lte=to_date)
        ).distinct()

    return render(request, 'adminsection/bwdates_reports_ds.html',
                  context={'invoice_list': invoice_list,
                            'from_date': from_date,
                            'to_date': to_date
                           })


@staff_member_required
def adminprofile(request):
    return render(request, 'adminsection/admin_profile.html')


@staff_member_required
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'adminsection/change_password.html', context={'form': form})


def forgetpassword(request):
    return render(request, 'adminsection/forget_password.html')

# def logout(request):
#     auth.logout(request)
#     return redirect('login')


def contactus(request):
    return render(request, 'adminsection/contact_us.html')
