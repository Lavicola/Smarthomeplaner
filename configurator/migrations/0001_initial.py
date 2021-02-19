# Generated by Django 3.1.4 on 2021-02-19 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_remove_customuser_last_visit'),
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
