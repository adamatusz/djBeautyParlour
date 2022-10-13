from django.contrib.auth.models import User
from django.db import models
from adminsection.models import Service
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
# class User(models.Model):
#     Name = models.CharField(max_length=50)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    PhoneNumber = models.CharField(max_length=11)
    Service = models.ManyToManyField(Service)
    Note = models.TextField(blank=False, null=False)
    AppointmentDate = models.DateField()
    AppointmentTine = models.TimeField()
    ApplyDate = models.DateTimeField(auto_now_add=True)
    RemarkDate = models.DateTimeField(auto_now=True)
    AppointmentNumber = models.IntegerField(null=True, blank=True)
    REMARK_CHOICES = (
        ('1', 'Accepted'),
        ('0', 'Rejected'),
        ('', 'Waiting')
    )
    Remark = models.CharField(max_length=1, choices=REMARK_CHOICES)

    def __str__(self):
        return self.Name


@receiver(post_save, sender=Appointment)
def appointment_listing_update(sender, instance, created, **kwargs):
    appointmentnumber = 6000
    if created:
        instance.AppointmentNumber = appointmentnumber + instance.id
        instance.save()

