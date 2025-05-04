from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    # Password Management
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),

    # Classrooms
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('classrooms/', views.view_classrooms, name='view_classrooms'),
    path('classrooms/add/', views.add_classroom, name='add_classroom'),
    path('classrooms/edit/<int:classroom_id>/', views.edit_classroom, name='edit_classroom'),
    path('classrooms/delete/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),

    # Students
    path('students/', views.view_students, name='student_list'),
    path('students/<int:pk>/', views.student_details, name='student_details'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('students/<int:student_id>/marks/', views.student_marks, name='student_marks'),
    path('students/<int:student_id>/add_mark/', views.add_mark, name='add_mark'),
    path('students/<int:student_id>/edit_mark/<int:mark_id>/', views.edit_mark, name='edit_mark'),

    #attendance
   path('student/<int:pk>/attendance/', views.mark_attendance, name='mark_attendance'),


]
