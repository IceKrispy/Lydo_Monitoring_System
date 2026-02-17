from django.db import models
from django.utils import timezone


class Barangay(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    # NOTICE: This class is NOT indented. It aligns with "class Barangay".
class Youth(models.Model):
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=50) 
    program = models.CharField(max_length=200, blank=True, null=True)
    date_enrolled = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.barangay.name})"


# Create your models here.
