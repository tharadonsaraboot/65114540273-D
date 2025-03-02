from django.db import models

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField()
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"