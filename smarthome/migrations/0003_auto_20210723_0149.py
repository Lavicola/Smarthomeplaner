# Generated by Django 3.2.5 on 2021-07-22 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0002_auto_20210723_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connector',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='dataprotectioninformation',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]