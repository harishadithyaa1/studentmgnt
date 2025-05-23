# Generated by Django 5.1.7 on 2025-04-04 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_classroom_teacher_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grade', models.CharField(max_length=2)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.student')),
            ],
        ),
    ]
