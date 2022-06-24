
from django.shortcuts import render

from api.models import Attendance, Student

def index(request):

    attendances = Attendance.objects.all()
    students = []
    
    for attendance in attendances:
        if attendance.user_type == "Student":
            student = Student.objects.filter(first_name=attendance.name)
            students.append(student)
        
    return render(request, 'core/index.html',
        {
            'students': students,
            'attendances': attendances,
            'page': 'home',
        })