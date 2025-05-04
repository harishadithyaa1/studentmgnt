from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher, Classroom, Student, Marks, Attendance
from .forms import TeacherForm, ClassroomForm, StudentForm, LoginForm, RegisterForm, AttendanceForm, AttendanceFormSet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect logged-in users away from login page

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Set session expiry if "Remember Me" is not checked
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires on browser close

                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'base/register.html', {'form': form})


@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'base/add_teacher.html', {'form': form})

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    for teacher in teachers:
        teacher.classroom_count = teacher.classrooms.count()  # Ensure this field is available
    form = TeacherForm()  # Create an instance of the form
    return render(request, 'base/teacher_list.html', {'teachers': teachers, 'form': form})

@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        teacher.name = request.POST.get('name')
        teacher.email = request.POST.get('email')
        teacher.phone_number = request.POST.get('phone_number')  # ✅ must match the input field name
        teacher.save()
        return redirect('teacher_list')
    
    return render(request, 'base/edit_teacher.html', {'teacher': teacher})

@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    return redirect('teacher_list')


@login_required
def add_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('classroom_list')
    else:
        form = ClassroomForm()
    return render(request, 'base/add_classroom.html', {'form': form})

@login_required
def classroom_list(request):
    classrooms = Classroom.objects.all()
    form = ClassroomForm()

    if request.method == "POST":
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('classroom_list') 

    return render(request, 'base/classroom_list.html', {'classrooms': classrooms, 'form': form})

@login_required
def edit_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        classroom.name = request.POST.get('name')
        classroom.room_number = request.POST.get('room_number')
        teacher_id = request.POST.get('teacher')
        classroom.teacher = get_object_or_404(Teacher, id=teacher_id)
        classroom.save()
        return redirect('classroom_list')

    return render(request, 'base/edit_classroom.html', {'classroom': classroom, 'teachers': teachers})

@login_required
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    classroom.delete()
    return redirect('classroom_list')


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'base/add_student.html', {'form': form})

from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student, Marks

@login_required
def student_list(request):
    query = request.GET.get('q', '').strip()

    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

        if students.count() == 1:
            student = students.first()
            return redirect('student_details', pk=student.pk)  # 👈 redirect instead of render

        if students.count() == 0:
            return render(request, 'base/student_list.html', {
                'students': [],
                'query': query,
                'no_results': True
            })

        # If more than one student matches, you can still show list
        return render(request, 'base/student_list.html', {
            'students': students,
            'query': query
        })

    students = Student.objects.all()
    return render(request, 'base/student_list.html', {
        'students': students,
        'query': query
    })


@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    classrooms = Classroom.objects.all()

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')  
        student.dob = request.POST.get('dateofbirth')  
        classroom_id = request.POST.get('classroom')
        student.classroom = get_object_or_404(Classroom, id=classroom_id)
        student.save()
        return redirect('student_list')

    return render(request, 'base/edit_student.html', {'student': student, 'classrooms': classrooms})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')

@login_required
def student_marks(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks = Marks.objects.filter(student=student)
    return render(request, 'base/student_marks.html', {
        'student': student,
        'marks': marks
    })

@login_required
def add_mark(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        subject = request.POST['subject']
        score = request.POST['score']
        grade = request.POST['grade']
        Marks.objects.create(student=student, subject=subject, score=score, grade=grade)
    return redirect('student_marks', student_id=student.id)

@login_required
def edit_mark(request, student_id, mark_id):
    student = get_object_or_404(Student, id=student_id)
    mark = get_object_or_404(Marks, id=mark_id)

    if request.method == 'POST':
        mark.subject = request.POST['subject']
        mark.score = request.POST['score']
        mark.grade = request.POST['grade']
        mark.save()
        return redirect('student_marks', student_id=student.id)

    return render(request, 'base/edit_mark.html', {
        'student': student,
        'mark': mark
    })

@login_required
def view_students(request):
    students = Student.objects.all()  # Retrieve all students from the database
    return render(request, 'base/view_students.html', {'students': students})

@login_required
def view_classrooms(request):
    classrooms = Classroom.objects.all()
    classroom_form = ClassroomForm()
    teacher_form = TeacherForm()  # Add TeacherForm

    return render(request, 'base/view_classrooms.html', {
        'classrooms': classrooms,
        'classroom_form': classroom_form,
        'teacher_form': teacher_form  # Pass TeacherForm to the template
    })  

@login_required
def student_details(request, pk):
    student = Student.objects.get(pk=pk)
    last_mark = Marks.objects.filter(student=student).order_by('-id').first()

    return render(request, 'base/student_details.html', {
        'student': student,
        'last_mark': last_mark
    })


def mark_attendance(request, pk):
    student = Student.objects.get(pk=pk)
    error = None

    if request.method == 'POST':
        try:
            present_days = int(request.POST.get('present_days'))
            total_days = int(request.POST.get('total_days'))

            student.present_days = present_days
            student.total_days = total_days
            student.save()
        except Exception as e:
            error = str(e)

    return render(request, 'base/mark_attendance.html', {'student': student, 'error': error})
