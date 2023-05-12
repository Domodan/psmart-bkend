from datetime import datetime, timedelta, date
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import json, math

from api.models import Attendance, Student, Teacher, Timetable, Subject
from core.forms import Student_Form, Teacher_Form

def get_total_hours_timetable(subject, term_start, term_end):
    total_hours = timedelta()
    # entries = Timetable.objects.filter(subject=subject)
    entries = Timetable.objects.filter(title__contains=subject)
    for entry in entries:
        total_hours += entry.end - entry.start
    return total_hours.total_seconds() / 3600  # convert to hours

def get_total_hours_attendance(subject, unique_id):
    total_hours = timedelta()
    attendances = Attendance.objects.filter(unique_id=unique_id, subject=subject)
    for attendance in attendances:
        total_hours += attendance.time_out - attendance.time_in
    return total_hours.total_seconds() / 3600  # convert to hours


def index(request):
    return render(request, 'core/index.html',
        {
            'page': 'home',
        })


@login_required      
def users(request):
    users = []
    teachers = Teacher.objects.all()
    students = Student.objects.all()

    for teacher in teachers:
        users.append(teacher)
    for student in students:
        users.append(student)

    return render(request, 'core/all_users.html',
        {
            'users': users,
            'page': 'all_users',
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
def attendance(request, user_type=None):

    user_data = []

    if user_type == "students":
        attendances = Attendance.objects.filter(user_type = "student")
        for attendance in attendances:
            print("Attendance Unique ID:", attendance.unique_id)
            print("Attendance Name:", attendance.name)
            student = Student.objects.get(unique_id=attendance.unique_id)
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
    print("Request Data:", request.POST)
    if request.method == 'POST':
        student_count = Student.objects.all().count()
        current_date = datetime.today()
        reg_number = str(current_date.year) + "/" + "STD/" + str(student_count + 1)

        post_data = request.POST.copy()
        post_data['unique_id'] = reg_number
        print("Post Data:", request.POST)
        print("Post Data Copy:", post_data)
        request.POST = post_data
        print("Post Data 2:", request.POST)
        print("Post Data Files:", request.FILES)

        student = Student_Form(request.POST, request.FILES)
        print("Student Data Valid:", student.is_valid())
        if student.is_valid():
            first_name = student.cleaned_data['first_name']
            last_name = student.cleaned_data['last_name']
            unique_id = student.cleaned_data['unique_id']

            old_student = Student.objects.filter(first_name=first_name, last_name=last_name, unique_id=unique_id)

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
def student_profile(request, pk=None):
    student_profile = Student.objects.get(pk=pk)
    unique_id = student_profile.unique_id
    attendances = Attendance.objects.filter(user_type = "student", unique_id=unique_id)

    total_hours_attendance = timedelta()
    for attendance in attendances:
        total_hours_attendance += attendance.time_out - attendance.time_in

    actual_total_hours = timedelta()
    timetable_obj = Timetable.objects.filter(created_at__year=2023)
    for timetable in timetable_obj:
        actual_total_hours += timetable.end - timetable.start

    attendance_percentage = math.floor((total_hours_attendance / actual_total_hours) * 100 + 0.5)

    subjects = []
    subjects_attended = []
    total_hours_subject = timedelta()
    total_subject_hours_attended = timedelta()
    term_start = datetime(2023, 5, 1)
    term_end = datetime(2023, 12, 31)

    # Calculate the total hours for each subject
    subjects_obj = Subject.objects.all()
    for subject in subjects_obj:
        hours = get_total_hours_timetable(subject.name, term_start, term_end)
        subjects.append((subject.name, hours))
        total_hours_subject += timedelta(hours=hours)

        hours = get_total_hours_attendance(subject.name, unique_id=unique_id)
        subjects_attended.append((subject.name, hours))
        total_subject_hours_attended += timedelta(hours=hours)

    data = []

    # Calculate the percentage of time each subject was taught
    for i, (subject, hours) in enumerate(subjects):
        for j, (subject_, hour_) in enumerate(subjects_attended):
            newData = {}
            percent = 0.0
            if subject == subject_:
                if hours and hour_:
                    percent = hours / total_hours_subject.total_seconds() * 100
                hour_delta = timedelta(hours=hour_)
                newData['subject'] = subject_
                newData['hours'] = hour_
                newData['percent'] = round(percent, 2)
                newData['hours_spent'] = str(hour_delta).split('.')[0]
                data.append(newData)
    
    return render(request, 'core/student_profile.html',
    {
        'student_profile': student_profile,
        'data': data,
        'subjects': subjects_obj,
        'attendance_percentage': attendance_percentage,
        'page': 'student_profile'
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
        post_data['unique_id'] = reg_number
        request.POST = post_data

        teacher = Teacher_Form(request.POST, request.FILES)

        if teacher.is_valid():
            first_name = teacher.cleaned_data['first_name']
            last_name = teacher.cleaned_data['last_name']
            unique_id = teacher.cleaned_data['unique_id']
            email = teacher.cleaned_data['email']

            old_teacher = Teacher.objects.filter(first_name=first_name, last_name=last_name, email=email, unique_id=unique_id)

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
def teacher_profile(request, pk=None):
    teacher_profile = Teacher.objects.get(pk=pk)
    unique_id = teacher_profile.unique_id
    attendances = Attendance.objects.filter(user_type = "teacher", unique_id=unique_id)
    
    print("Unique ID:", unique_id)
    print("Attendances:", attendances)
    print("Teacher Profile:", teacher_profile)

    total_hours_attendance = timedelta()
    for attendance in attendances:
        total_hours_attendance += attendance.time_out - attendance.time_in
    
    hours_ = total_hours_attendance // timedelta(hours=1)
    minutes = (total_hours_attendance - timedelta(hours=hours_)) // timedelta(minutes=1)
    seconds = (total_hours_attendance - timedelta(hours=hours_, minutes=minutes)) // timedelta(seconds=1)
    hours_spent = f"{hours_}-Hours {minutes}-Minutes {seconds}-Seconds"

    actual_total_hours = timedelta()
    timetable_obj = Timetable.objects.filter(created_at__year=2023)
    for timetable in timetable_obj:
        actual_total_hours += timetable.end - timetable.start

    attendance_percentage = math.floor((total_hours_attendance / actual_total_hours) * 100 + 0.5)

    subjects = []
    subjects_attended = []
    total_hours_subject = timedelta()
    total_subject_hours_attended = timedelta()
    term_start = datetime(2023, 5, 1)
    term_end = datetime(2023, 12, 31)

    # Calculate the total hours for each subject
    for subject in teacher_profile.subject.all():
        hours = get_total_hours_timetable(subject.name, term_start, term_end)
        subjects.append((subject.name, hours))
        total_hours_subject += timedelta(hours=hours)

        hours = get_total_hours_attendance(subject.name, unique_id=unique_id)
        subjects_attended.append((subject.name, hours))
        total_subject_hours_attended += timedelta(hours=hours)

    data = []

    # Calculate the percentage of time each subject was taught
    for i, (subject, hours) in enumerate(subjects):
        for j, (subject_, hour_) in enumerate(subjects_attended):
            newData = {}
            percent = 0.0
            if subject == subject_:
                if hours and hour_:
                    percent = hours / total_hours_subject.total_seconds() * 100
                hour_delta = timedelta(hours=hour_)
                # total_seconds = hour_delta.total_seconds()
                # hourss = int(total_seconds // 3600)
                # minutess = int((total_seconds % 3600) // 60)
                # timespent = f"{hourss}-Hours {minutess}-Minutes"
                # print("Time Spent:", timespent)
                newData['subject'] = subject_
                newData['hours'] = hour_
                newData['percent'] = round(percent, 2)
                newData['hours_spent'] = str(hour_delta).split('.')[0]
                data.append(newData)
        subjects[i] = (subject, str(timedelta(hours=hours)), percent)
    
    print('percent_teaching_time',
          round(total_hours_subject.total_seconds() / ((term_end - term_start).total_seconds() / 100), 2))

    print("Data:", data)
    return render(request, 'core/teacher_profile.html',
    {
        'teacher_profile': teacher_profile,
        'data': data,
        'attendance_percentage': attendance_percentage,
        'page': 'teacher_profile'
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


def calendar(request):
    calendar_obj = Timetable.objects.all()
    serialized = serialize('json', calendar_obj)

    serializer = json.loads(serialized)
    print("Serializer:", serializer)

    calendar_data = []

    # print("Calendar Object:", calendar_obj)
    # print("Calendar Serialized:", serialized)

    for calendar in calendar_obj:
        calendar_data.append(calendar)
        print("Calendar:", calendar)

    print("Calendar Data:", calendar_data)
    return render(request, 'core/calendar.html',
        {
            'page': 'calendar',
            'calendar': calendar_data,
        })


def get_timetable_events(request):
    timetable = Timetable.objects.all()
    serialized = serialize('json', timetable)

    calendar_data = []

    for calendar in timetable:
        calendar_data.append(calendar)
        print("Calendar:", calendar)

    serialized2 = serialize('json', calendar_data)
    print("Serialized:", serialized)
    print("Serialized2:", serialized2)
    return JsonResponse(serialized2, safe=False)


def term_hours(request):
    term_start = datetime(2023, 9, 1) # replace with the start date of your term
    term_end = datetime(2023, 12, 31) # replace with the end date of your term

    # Get a list of all unique subjects in the timetable
    subjects = Timetable.objects.values_list('subject', flat=True).distinct()

    # Calculate the total hours for each subject
    subject_hours = []
    total_hours = timedelta()
    for subject in subjects:
        hours = get_total_hours_timetable(subject, term_start, term_end)
        subject_hours.append((subject, hours))
        total_hours += timedelta(hours=hours)

    # Format the total hours as H:M:S
    total_hours_str = str(total_hours).split('.')[0]

    # Calculate the percentage of time each subject was taught
    for i, (subject, hours) in enumerate(subject_hours):
        percent = hours / total_hours.total_seconds() * 100
        subject_hours[i] = (subject, str(timedelta(hours=hours)), percent)

    # Render the template
    context = {
        'term_start': term_start,
        'term_end': term_end,
        'subject_hours': subject_hours,
        'total_hours': total_hours_str,
        'percent_teaching_time': round(total_hours.total_seconds() / ((term_end - term_start).total_seconds() / 100), 2),
    }

