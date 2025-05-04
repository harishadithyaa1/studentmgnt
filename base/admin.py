from django.contrib import admin
from .models import Teacher, Classroom, Student, Attendance

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'hire_date')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('hire_date',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_number', 'teacher')
    search_fields = ('name', 'room_number')
    list_filter = ('teacher',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'dob', 'classroom', 'teacher', 'attendance_percentage')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('classroom', 'teacher', 'dob')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('student__first_name', 'student__last_name')