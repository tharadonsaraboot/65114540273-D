from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Course
from .forms import CourseForm

def course_management(request, course_code=None):
    # ดึงข้อมูลรายวิชาทั้งหมด
    courses = Course.objects.all()
    course = None
    form = None
    error_message = None
    success_message = None
    search_results = None
    mode = request.GET.get('mode', 'list')  # list, edit, create, search, search_name, delete
    
    # กรณีค้นหารายวิชาจากรหัสวิชา
    if request.method == 'POST' and 'search_code' in request.POST:
        search_code = request.POST.get('course_code')
        try:
            course = Course.objects.get(course_code=search_code)
            return redirect(f'/courses/{course.course_code}/?mode=edit')
        except Course.DoesNotExist:
            error_message = f"ไม่พบรายวิชารหัส {search_code}"
            mode = 'search'
    
    # กรณีค้นหารายวิชาจากชื่อวิชา
    elif request.method == 'POST' and 'search_name' in request.POST:
        search_name = request.POST.get('course_name')
        search_results = Course.objects.filter(course_name__icontains=search_name)
        if not search_results:
            error_message = f"ไม่พบรายวิชาที่มีชื่อคล้ายกับ '{search_name}'"
        mode = 'search_name'
    
    # กรณีลบรายวิชา
    elif request.method == 'POST' and 'delete' in request.POST:
        course_code_to_delete = request.POST.get('course_code')
        try:
            course = Course.objects.get(course_code=course_code_to_delete)
            course_name = course.course_name
            course.delete()
            success_message = f"ลบรายวิชา {course_code_to_delete} - {course_name} เรียบร้อยแล้ว"
            return redirect('/courses/?mode=list&message=delete_success')
        except Course.DoesNotExist:
            error_message = f"ไม่พบรายวิชารหัส {course_code_to_delete}"
            mode = 'delete'
    
    # กรณีสร้างหรือแก้ไขรายวิชา
    elif request.method == 'POST' and ('create' in request.POST or 'edit' in request.POST):
        if course_code:  # แก้ไข
            course = get_object_or_404(Course, course_code=course_code)
            form = CourseForm(request.POST, instance=course)
            success_message = f"แก้ไขข้อมูลรายวิชา {course_code} เรียบร้อยแล้ว"
        else:  # สร้างใหม่
            form = CourseForm(request.POST)
            success_message = "เพิ่มรายวิชาใหม่เรียบร้อยแล้ว"
        
        if form.is_valid():
            form.save()
            return redirect('/courses/?message=save_success')
        
        mode = 'edit' if course_code else 'create'
    
    # กรณีเตรียมฟอร์มสำหรับสร้างหรือแก้ไข
    elif mode == 'edit' and course_code:
        course = get_object_or_404(Course, course_code=course_code)
        form = CourseForm(instance=course)
    elif mode == 'create':
        form = CourseForm()
    
    # ตรวจสอบข้อความสำเร็จจาก URL parameter
    if request.GET.get('message') == 'save_success':
        success_message = "บันทึกข้อมูลเรียบร้อยแล้ว"
    elif request.GET.get('message') == 'delete_success':
        success_message = "ลบรายวิชาเรียบร้อยแล้ว"
    
    return render(request, 'courses/course_management.html', {
        'courses': courses,
        'course': course,
        'form': form,
        'error_message': error_message,
        'success_message': success_message,
        'search_results': search_results,
        'mode': mode
    })