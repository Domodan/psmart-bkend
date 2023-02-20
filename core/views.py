from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required

from api.models import Attendance, Student, Teacher
from core.forms import Student_Form, Teacher_Form


def index(request):
    return render(request, 'core/index.html',
        {
            'page': 'home',
        })


def add_user(request):
    return render(request, 'core/add_user.html',
        {
            'page': 'add_user',
        })


def sign_up(request):
    return render(request, 'core/authentication-signup-basic.html',
        {
            'page': 'sign_up',
        })


@login_required
def attendance(request, user_type=None):

    user_data = []

    if user_type == "students":
        attendances = Attendance.objects.filter(user_type = "student")
        for attendance in attendances:
            student = Student.objects.get(first_name=attendance.name)
            user_data.append(({ 'attendance': attendance, 'student': student,}))
        return render(request, 'core/students_attendance.html',
            {
                'students': user_data,
                'page': 'attendance_students',
            })
    elif user_type == "teachers":
        attendances = Attendance.objects.filter(user_type = "teacher")
        for attendance in attendances:
            teacher = Teacher.objects.get(unique_id=attendance.unique_id)
            user_data.append(({ 'attendance': attendance, 'teacher': teacher}))
        return render(request, 'core/teachers_attendance.html',
            {
                'teachers': user_data,
                'page': 'attendance_teachers',
            })


@login_required      
def users(request):
    users = []
    return render(request, 'core/all_users.html',
        {
            'users': users,
            'page': 'all_users',
        })

        
def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['admin_id'] = user.id
            return redirect('students')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('sign_in')
    else:
        return render(request, 'core/authentication-login-basic.html',
            {
                'page': 'login',
            })

    '''

            
        {% if user.is_authenticated %}
        <li class="nav-item">
          <a class="nav-link" href="#">Hi, {{user.first_name}}</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="logout_user">LOGOUT</a>
        </li>
        {% else %}
        <li class="nav-item">
          <a class="nav-link" href="register">SIGN UP</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="login_user">LOGIN</a>
        </li>
        {% endif %}
    
    '''

        
def sign_out(request):
    admin_id = request.session.get('admin_id', None)
    print("Admin ID:", admin_id)
    if admin_id is not None:
        auth.logout(request)
        try:
            del request.session['admin_id']
        except:
            pass
    else:
        auth.logout(request)
    return redirect('index')

    '''

            
        {% if user.is_authenticated %}
        <li class="nav-item">
          <a class="nav-link" href="#">Hi, {{user.first_name}}</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="logout_user">LOGOUT</a>
        </li>
        {% else %}
        <li class="nav-item">
          <a class="nav-link" href="register">SIGN UP</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="login_user">LOGIN</a>
        </li>
        {% endif %}
    
    '''


@login_required
def students(request):
    if request.method == 'POST':
        print("It's a post method")
    else:
        student = Student.objects.all()

    return render(request, 'core/students.html',
        {
            'students': student,
            'page': 'students',
        }
    )


@login_required  
def add_students(request):

    if request.method == 'POST':
        student_count = Student.objects.all().count()
        current_date = datetime.today()
        reg_number = str(current_date.year) + "/" + "STD/" + str(student_count + 1)

        post_data = request.POST.copy()
        post_data['registration_number'] = reg_number
        request.POST = post_data

        student = Student_Form(request.POST, request.FILES)

        if student.is_valid():
            first_name = student.cleaned_data['first_name']
            last_name = student.cleaned_data['last_name']
            registration_number = student.cleaned_data['registration_number']

            old_student = Student.objects.filter(first_name=first_name, last_name=last_name, registration_number=registration_number)

            if old_student.exists():
                messages.info(request, "Error, Student already exist, please try again")
                return render(request, 'core/students_add.html',
                    {
                        'student': student,
                        'page': 'add_students',
                    }
                )
            else:
                student.save()
                return HttpResponseRedirect(reverse('students'))
        else:
            messages.info(request, 'Error, could not add student, please try again')
            return render(request, 'core/students_add.html',
                {
                    'student': student,
                    'page': 'add_students',
                }
            )
    else:
        student = Student_Form()
        return render(request, 'core/students_add.html', {
            'student': student,
            'page': 'add_students',
        })


@login_required
def teachers(request):
    if request.method == 'POST':
        print("It's a post method")
    else:
        teacher = Teacher.objects.all()

    return render(request, 'core/teachers.html',
        {
            'teachers': teacher,
            'page': 'teachers',
        }
    )


@login_required  
def add_teachers(request):
    print("Request Object:", request.POST)
    print("Request File Object:", request.FILES)

    if request.method == 'POST':
        teacher_count = Teacher.objects.all().count()
        current_date = datetime.today()
        reg_number = str(current_date.year) + "/" + "TR/" + str(teacher_count + 1)

        post_data = request.POST.copy()
        post_data['staff_number'] = reg_number
        request.POST = post_data

        teacher = Teacher_Form(request.POST, request.FILES)

        if teacher.is_valid():
            first_name = teacher.cleaned_data['first_name']
            last_name = teacher.cleaned_data['last_name']
            staff_number = teacher.cleaned_data['staff_number']
            email = teacher.cleaned_data['email']

            old_teacher = Teacher.objects.filter(first_name=first_name, last_name=last_name, email=email, staff_number=staff_number)

            if old_teacher.exists():
                messages.info(request, "Error, Teacher already exist, please try again")
                return render(request, 'core/teachers_add.html',
                    {
                        'teacher': teacher,
                        'page': 'add_teachers',
                    }
                )
            else:
                teacher.save()
                return HttpResponseRedirect(reverse('teachers'))
        else:
            messages.info(request, 'Error, could not add teacher, please try again')
            return render(request, 'core/teachers_add.html',
                {
                    'teacher': teacher,
                    'page': 'add_teachers',
                }
            )
    else:
        teacher = Teacher_Form()
        return render(request, 'core/teachers_add.html', {
            'teacher': teacher,
            'page': 'add_teachers',
        })


@login_required
def all_admin(request):

    admins = User.objects.all()
    for admin in admins:
        print("Users:", admin)
        print("First Name:", admin.first_name)
        print("Last Name:", admin.last_name)
        print("Last Name:", admin.profile.avatar)

    attendances = Attendance.objects.all()
    user_data = []
    
    for attendance in attendances:
        if attendance.user_type == "Student":
            student = Student.objects.get(first_name=attendance.name)
            print("Student Type:", type(student))
            print("Attendance Type:", type(attendance))
            user_data.append(({ 'attendance': attendance, 'student': student,}))    

    for data in user_data:
        print("Student:", data['student'])
        print("Attendance:", data['attendance'])
        print("Student Name:", data['student'].first_name)
        print("Attendance Name:", data['attendance'].name)

    return render(request, 'core/all_admin.html',
        {
            'admins': admins,
            'page': 'admins',
        })


@login_required
def user_profile(request, pk=None):
    print("PK:", pk)
    user_profile = User.objects.get(pk=pk)
    
    print("User Profile:", user_profile)
    print("User ID:", user_profile.id)
    print("Avatar:", user_profile.profile.avatar)

    return render(request, 'core/user_profile.html',
    {
        'user_profile': user_profile,
        'page': 'user_profile'
    })

@login_required
def teacher_profile(request, pk=None):
    teacher_profile = Teacher.objects.get(pk=pk)
    unique_id = teacher_profile.unique_id
    attendances = Attendance.objects.filter(user_type = "teacher", unique_id=unique_id)

    print("Unique ID:", unique_id)
    print("Attendances:", attendances)

    return render(request, 'core/teacher_profile.html',
    {
        'teacher_profile': teacher_profile,
        'page': 'teacher_profile'
    })

@login_required
def student_profile(request, pk=None):
    print("PK:", pk)
    student_profile = Student.objects.get(pk=pk)
    
    print("Student Profile:", student_profile)
    print("Student ID:", student_profile.id)
    print("Avatar:", student_profile.avatar)

    return render(request, 'core/student_profile.html',
    {
        'student_profile': student_profile,
        'page': 'student_profile'
    })

