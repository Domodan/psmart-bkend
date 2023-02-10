# Generated by Django 4.0 on 2023-01-28 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_attendance_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='subject2',
            field=models.CharField(choices=[('ENG', 'English'), ('MTC', 'Mathematics'), ('SCI', 'Science'), ('SST', 'Social Studies')], default='English', max_length=20),
        ),
    ]
