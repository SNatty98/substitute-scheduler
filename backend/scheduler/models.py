from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    SUBSTITUTE = 'substitute'

    ROLE_CHOICES = [
        (ADMIN, 'School Admin'),
        (SUBSTITUTE, 'Substitute Teacher'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Substitute(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='substitute_profile')
    postcode = models.CharField(max_length=10)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=20)
    subjects = models.JSONField(default=list)
    qualifications = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {', '.join(self.subjects)}"


class Assignment(models.Model):
    OPEN = 'open'
    FILLED = 'filled'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (FILLED, 'Filled'),
        (CANCELLED, 'Cancelled'),
    ]

    school_name = models.CharField(max_length=40)
    school_postcode = models.CharField(max_length=10)
    school_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    school_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    year_group = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=OPEN)

    selected_substitute = models.ForeignKey(
        Substitute,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_assignments'
    )

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.subject} at {self.school_name} on {self.date}"


class Application(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepting'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    ]

    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='applications')
    substitute = models.ForeignKey(
        Substitute, on_delete=models.CASCADE, related_name='application')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PENDING)
    message = models.TextField(blank=True)
    distance_miles = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['assignment', 'substitute']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.substitute.user.get_full_name()} -> {self.assignment.subject}"
