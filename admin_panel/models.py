from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Institute(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True)  # Auto-generated like VD_01, VD_02, etc.
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='institute_images/')
    admin_password = models.CharField(max_length=100)  # Password set by admin while creating institute

    def __str__(self):
        return self.name



class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.OneToOneField(Institute, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    
    
    

class CourseFee(models.Model):
    COURSE_CHOICES = (
        ('BSE', 'BSE'),
        ('CBSE', 'CBSE'),
        ('Competitive', 'Competitive'),
    )

    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    class_name = models.CharField(max_length=20)  # New field for class name
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  # Duration field
    subject = models.CharField(max_length=100)  # Subject field
    qualification = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course} - {self.class_name} - {self.fee_amount}"
