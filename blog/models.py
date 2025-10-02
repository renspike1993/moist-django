from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    course = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    alternative_contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.full_name
