from django import forms
from django.contrib.auth.models import User

from api.models import Profile, Student, Teacher

# User Login Form
class User_Login(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'password' ]

# User Registry Form
class User_Register_Form(forms.ModelForm):

    class Meta:
        model = User
        exclude = ( 'groups', 'permissions' )

# User Update Form
class User_Update_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'password', 'email', 'first_name', 'last_name' ]


# Create User Profile
# class Profile_Create_Form(forms.ModelForm):
#     class Meta:
#         exclude = ( 'groups', 'permissions' )


# Update Profile
# class Profile_Update_Form(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['school', 'phone_number', 'position', 'avatar']


'''
Teacher Related Forms
'''

# Teacher Form
class Teacher_Form(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name: John',
                'class': 'form-control form-control-lg',
                'aria-label': 'John',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name: Doe',
                'class': 'form-control form-control-lg',
                'aria-label': 'Doe'
            }),
            'gender': forms.TextInput(attrs={
                'placeholder': 'Female',
                'class': 'form-control form-control-lg',
                'aria-label': 'Female'
            }),
            'subject': forms.SelectMultiple(attrs={
                'placeholder': 'English',
                'class': 'form-control form-control-lg',
                'aria-label': 'English'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': "someone@example.com",
                'class': 'form-control form-control-lg',
                'aria-label': "someone@example.com",
                'type': 'email'
            }),
            'phone': forms.NumberInput(attrs={
                'placeholder': 'e.g. 0772814507',
                'class': 'form-control form-control-lg',
                'aria-label': 'e.g. 0772814507'
            }),
            'school': forms.TextInput(attrs={
                'placeholder': 'Your School',
                'class': 'form-control form-control-lg',
                'aria-label': 'Your School'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'js-file-attach form-attachment-btn-label',
                "data-hs-file-attach-options": {
                    "textTarget": "#avatarImg",
                    "mode": "image",
                    "targetAttr": "src",
                    "resetTarget": ".js-file-attach-reset-img",
                    "resetImg": "{% static 'core/assets/img/160x160/img1.jpg' %}",
                    "allowedTypes": [".png", ".jpeg", ".jpg"]
                }
            }),
            'unique_id': forms.TextInput(attrs={
                'placeholder': "Registration Number",
                'class': 'form-control form-control-lg',
                'aria-label': "Registration Number"
            }),
        }


'''
Student Related Forms
'''

# Student Form
class Student_Form(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name: John',
                'class': 'form-control form-control-lg',
                'aria-label': 'John',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name: Doe',
                'class': 'form-control form-control-lg',
                'aria-label': 'Doe'
            }),
            'gender': forms.TextInput(attrs={
                'placeholder': 'Female',
                'class': 'form-control form-control-lg',
                'aria-label': 'Female'
            }),
            'student_class': forms.TextInput(attrs={
                'placeholder': 'S.6 or P.1',
                'class': 'form-control form-control-lg',
                'aria-label': 'S.6 or P.1'
            }),
            'school': forms.TextInput(attrs={
                'placeholder': 'Your School',
                'class': 'form-control form-control-lg',
                'aria-label': 'Your School'
            }),
            'level': forms.TextInput(attrs={
                'placeholder': "Primary or O'Level",
                'class': 'form-control form-control-lg',
                'aria-label': "Primary or O'Level"
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'js-file-attach form-attachment-btn-label',
                "data-hs-file-attach-options": {
                    "textTarget": "#avatarImg",
                    "mode": "image",
                    "targetAttr": "src",
                    "resetTarget": ".js-file-attach-reset-img",
                    "resetImg": "{% static 'core/assets/img/160x160/img1.jpg' %}",
                    "allowedTypes": [".png", ".jpeg", ".jpg"]
                }
            }),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'unique_id': forms.TextInput(attrs={
                'placeholder': "Registration Number",
                'class': 'form-control form-control-lg',
                'aria-label': "Registration Number"
            }),
        }

