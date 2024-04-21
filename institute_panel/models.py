from django.db import models
from django.utils import timezone  
# Create your models here.
from django.db import models
from admin_panel.models import Institute,CourseFee

class Student(models.Model):
    ADMISSION_CHOICES = (
        ('BSE', 'BSE'),
        ('CBSE', 'CBSE'),
        ('Competitive', 'Competitive'),
    )
    
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    course = models.CharField(max_length=20, choices=ADMISSION_CHOICES)
    contact_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    admission_date = models.DateField(default=timezone.now)
    course_fee = models.ForeignKey(CourseFee, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_STATUS = (
        (1, "Payment Success"),
    )
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, default=1)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_fee = models.ForeignKey(CourseFee, on_delete=models.CASCADE, null=True, blank=True)
    payment_status = models.IntegerField(default=1, choices=PAYMENT_STATUS)  # Default to 1 for Success
    payment_date = models.DateTimeField(default=timezone.now)  # Date and time of payment
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_id = models.CharField(max_length=255, blank=True, null=True)  # Add this field for storing the order ID

    def __str__(self):
        return f"{self.student} - {self.get_payment_status_display()} - {self.payment_date}"
    
    
    
