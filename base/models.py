from django.db import models
from django.utils import timezone


class Teacher(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name  # Keep it simple for dropdowns


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms')  # Fix here
    room_number = models.CharField(max_length=50, default="Unknown")

    def __str__(self):
        return f"{self.name} - {self.room_number}"


class Student(models.Model):
    CLASSROOM_CHOICES = [
        ('A', 'Classroom A'),
        ('B', 'Classroom B'),
        ('C', 'Classroom C'),
    ]

    first_name = models.CharField(max_length=100, default="Unknown")
    last_name = models.CharField(max_length=100, default="Unknown")
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)  
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True) 
    present_days = models.IntegerField(default=0)
    total_days = models.IntegerField(default=0)
    attendance_percentage = models.FloatField(default=0.0)

    @property
    def attendance_percentage(self):
        if self.total_days == 0:
            return 0
        return (self.present_days / self.total_days) * 100

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    student = models.ForeignKey(Student, related_name='attendances', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
        
    
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)