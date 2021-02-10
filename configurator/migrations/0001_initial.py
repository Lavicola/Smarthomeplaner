# Generated by Django 3.1.4 on 2021-02-10 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanvasMap',
            fields=[
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser')),
                ('canvas_map', models.JSONField()),
            ],
        ),
    ]
