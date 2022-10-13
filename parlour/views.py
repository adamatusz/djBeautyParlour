from django.contrib.auth import (authenticate,
                                 login,
                                 logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (render,
                              get_object_or_404,
                              redirect)
from django.contrib import messages
from django.views import View

from parlour.forms import (AppointmentForm,
                           SignUpForm)
from parlour.models import Appointment
from adminsection.models import Service
from django.urls import reverse
from django.contrib.auth.hashers import make_password

# Create your views here.
#
# @login_required
# def home(request):
#     """
#         Provides the ability to make an appointment via user
#     """
#     services = Service.objects.all()
#     form = AppointmentForm(request.POST or None)
#
#     if request.method == 'POST':
#
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#             form.save_m2m()
#
#             return redirect(reverse("thankyou", kwargs={
#                 'id': form.instance.id
#             }))
#     return render(request, 'website/index.html',  context={'form': form, 'services': services})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You Have Been Logged In!!!'))
            return redirect('services')
        else:
            messages.success(request, ('Error Loggin In -Please Try Again...'))
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def logout_user(request):
        logout(request)
        messages.success(request, ('You Have Been Logged Out...'))
        return redirect('home')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        services = Service.objects.all()
        form = AppointmentForm()
        return render(request, 'website/index.html', context={'form': form, 'services': services})

    def post(self, request):
        form = AppointmentForm(request.POST)
        services = Service.objects.all()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save_m2m()

            return redirect(reverse("thankyou", kwargs={
                'id': form.instance.id
            }))
        return render(request, 'website/index.html', context={'form': form,
                                                              'services': services})


def services(request):
    """
        Listing Page for Services
    """
    services = Service.objects.all()
    return render(request, 'website/services.html', context={'services': services})


def thankyou(request, id):
    """
        Thankyou Page. Redirect here after customers make their appointment & get their appointmentnumber
    """
    appointmentid = get_object_or_404(Appointment, id=id)
    return render(request, 'website/thankyou.html', {'appointment': appointmentid})


def register_user(request):
    """Register a new user."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            u = form.save()
            login(request, u)
            messages.success(request, ('You Have Registered...'))
            return redirect('profile')
        # what if form is not valid?
        # we should display a message in register.html
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', context={'form': form})
# ________________________________________________

# class RegisterView(View):
#     def get(self, request):
#         form = SignUpForm()
#         return render(request, 'registration/register.html', context={'form': form})
#
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             u = form.save()
#             login(request, u)
#             messages.success(request, ('You Have Registered...'))
#             return redirect('profile')
# ________________________________________________


def edit_profile(request):
    """
        Edit profile
    """
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            u = form.save()
            login(request, u)
            messages.success(request, ('You Have Changed...'))
            return redirect('edit_profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', context={'form': form})


# class EditProfileView():
#     def get(self, request):
#         form = UserChangeForm(instance=request.user)
#         return render(request, 'registration/edit_profile.html', context={'form': form})
#
#     def post(self, request):
#         form = UserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             u = form.save()
#             login(request, u)
#             messages.success(request, ('You Have Changed...'))
#             return redirect('edit_profile')

def profile(request):
    form = UserCreationForm()
    return render(request, 'registration/profile.html', context={'form': form})