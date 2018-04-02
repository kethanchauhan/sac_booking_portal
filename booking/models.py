from django.db import models
import datetime
from sac_room.functions import send_parallel_mail

class InstituteBody(models.Model):
    body_name = models.CharField(blank=True, max_length=100)
    verification_email = models.CharField(blank=True, max_length=100)
    verified = models.BooleanField(default=False)
    verify_check = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)
    contact_number = models.CharField(blank=True, max_length=100)
    access_token = models.CharField(blank=True, max_length=100)
    refresh_token = models.CharField(blank=True, max_length=100)
    scope = models.CharField(blank=True, max_length=100)
    roll_number = models.CharField(blank=True, max_length=100)
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    is_admin = models.BooleanField(default=False)
    room_no = models.CharField(blank=True, max_length=10)
    hostel_name = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.roll_number

    def save(self, *args, **kwargs):
        super(InstituteBody, self).save(*args, **kwargs)
        if self.verified == True and self.verify_check == False:
            self.verify_check = True
            self.save()
            send_parallel_mail("Regarding Verification of your account", "Your account has been verified", [self.roll_number+'@iitb.ac.in'])

class SacRoom(models.Model):
    name = models.CharField(blank=True, max_length=100)
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.name)

class Booking(models.Model):
    STATUS_CHOICES = (
        ("pending", "pending"),
        ("approved", "approved"),
        ("rejected", "rejected")
    )
    sac_room = models.ForeignKey(SacRoom, null=True, on_delete=models.SET_NULL)
    booked_by = models.ForeignKey(InstituteBody, null = True, on_delete=models.SET_NULL)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="pending", max_length=100)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return str(self.sac_room.name)
