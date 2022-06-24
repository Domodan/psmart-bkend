
from django.shortcuts import render

from api.models import Attendance, Student

def index(request):

    attendances = Attendance.objects.all()
    students = []
    
    for i in attendances:
        attendance = attendances[i]
        if attendance['user_type'] == "Student":
            student = Student.objects.filter(name=attendance['name'])
            students.append(student)
        
    return render(request, 'core/index.html',
        {
            'students': students,
            'attendances': attendances,
            'page': 'home',
        })