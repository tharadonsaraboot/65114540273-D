from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
from .forms import CourseForm

def course_management(request, course_code=None):
    # ดึงข้อมูลรายวิชาทั้งหมด
    courses = Course.objects.all()
    course = None
    form = None
    error_message = None
    mode = request.GET.get('mode', 'list')  # list, edit, create, search
    
    # กรณีค้นหารายวิชา
    if request.method == 'POST' and 'search' in request.POST:
        search_code = request.POST.get('course_code')
        try:
            course = Course.objects.get(course_code=search_code)
            mode = 'edit'
        except Course.DoesNotExist:
            error_message = f"ไม่พบรายวิชารหัส {search_code}"
            mode = 'search'
    
    # กรณีสร้างหรือแก้ไขรายวิชา
    elif request.method == 'POST' and ('create' in request.POST or 'edit' in request.POST):
        if course_code:  # แก้ไข
            course = get_object_or_404(Course, course_code=course_code)
            form = CourseForm(request.POST, instance=course)
        else:  # สร้างใหม่
            form = CourseForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('course_management')
        
        mode = 'edit' if course_code else 'create'
    
    # กรณีเตรียมฟอร์มสำหรับสร้างหรือแก้ไข
    elif mode == 'edit' and course_code:
        course = get_object_or_404(Course, course_code=course_code)
        form = CourseForm(instance=course)
    elif mode == 'create':
        form = CourseForm()
    
    return render(request, 'courses/course_management.html', {
        'courses': courses,
        'course': course,
        'form': form,
        'error_message': error_message,
        'mode': mode
    })