from django import forms
from parlour.models import Appointment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = [
            'Name',
            'Email',
            'PhoneNumber',
            'Service',
            'AppointmentDate',
            'AppointmentTine',
        ]

    def clean_service(self):
        Service = self.cleaned_data.get('Service')

        if not Service:
            raise forms.ValidationError("Service is required")
        return Service


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Email Address'}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                         'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'placeholder': 'Last Name'
                                                                                        }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>'
        )
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<small><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></small'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<small>Enter the same password as before, for verification.</small>'


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User

        fields = ('username', 'first_name', 'last_name', 'email')


