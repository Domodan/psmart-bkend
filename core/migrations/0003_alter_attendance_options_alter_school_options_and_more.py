# Generated by Django 4.0 on 2022-06-14 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_attendance_school_student_teacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'verbose_name': 'Attendance', 'verbose_name_plural': 'Attendance'},
        ),
        migrations.AlterModelOptions(
            name='school',
            options={'verbose_name': 'School', 'verbose_name_plural': 'School'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Student'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Teacher', 'verbose_name_plural': 'Teacher'},
        ),
        migrations.AddField(
            model_name='attendance',
            name='user_type',
            field=models.CharField(default='Student', max_length=10),
        ),
    ]
