from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'credits', 'description', 'instructor']
        labels = {
            'course_code': 'รหัสวิชา',
            'course_name': 'ชื่อวิชา',
            'credits': 'หน่วยกิต',
            'description': 'คำอธิบายรายวิชา',
            'instructor': 'อาจารย์ผู้สอน',
        }