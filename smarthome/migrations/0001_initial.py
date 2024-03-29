# Generated by Django 3.1.4 on 2021-07-22 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connector', models.CharField(max_length=30)),
                ('connector_en', models.CharField(max_length=30, null=True)),
                ('connector_de', models.CharField(max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'Connector',
                'verbose_name_plural': 'Connectors',
            },
        ),
        migrations.CreateModel(
            name='DataProtectionInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('description_en', models.CharField(max_length=300, null=True)),
                ('description_de', models.CharField(max_length=300, null=True)),
                ('paper_url', models.URLField(max_length=500, verbose_name='URL to the Article to the Privacy Concern')),
            ],
            options={
                'verbose_name': 'Data Protection Information',
                'verbose_name_plural': 'Data Protection Information',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to='Device')),
                ('manufacturer', models.CharField(max_length=200)),
                ('generation', models.CharField(max_length=10)),
                ('category', models.CharField(choices=[('Smart_Lightning', 'Smart_Lightning'), ('Smart_Lock', 'Smart_Lock'), ('Virtual_Assistant', 'Virtual_Assistant')], max_length=20)),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='DeviceEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Device Entry',
                'verbose_name_plural': 'Device Entries',
            },
        ),
        migrations.CreateModel(
            name='Firmware',
            fields=[
                ('firmware_id', models.AutoField(primary_key=True, serialize=False)),
                ('version_number', models.CharField(max_length=50, verbose_name='Versionnumber')),
                ('changelog', models.CharField(max_length=500, verbose_name='Changelog')),
                ('changelog_en', models.CharField(max_length=500, null=True, verbose_name='Changelog')),
                ('changelog_de', models.CharField(max_length=500, null=True, verbose_name='Changelog')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Release Date')),
            ],
            options={
                'verbose_name': 'Firmware',
                'verbose_name_plural': 'Firmwares',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('standard', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Standard',
                'verbose_name_plural': 'Standard',
            },
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discovery', models.DateField(verbose_name='Vulnerability was found on:')),
                ('description', models.CharField(max_length=500, verbose_name='Description of the Vulnerability ')),
                ('description_en', models.CharField(max_length=500, null=True, verbose_name='Description of the Vulnerability ')),
                ('description_de', models.CharField(max_length=500, null=True, verbose_name='Description of the Vulnerability ')),
                ('paper_url', models.URLField(max_length=500, verbose_name='URL to the Article to the Vulnerability')),
                ('patch_date', models.DateField(blank=True, null=True, verbose_name='Vulnerability was patched on:')),
                ('url_patch', models.URLField(blank=True, max_length=500, verbose_name='URL to the Patch Article')),
                ('category', models.CharField(choices=[('Firmware', 'Firmware'), ('Physical', 'Physical'), ('Others', 'Others')], max_length=8)),
                ('device_id', models.ManyToManyField(to='smarthome.Device', verbose_name='Vulnerability exploitable by:')),
            ],
            options={
                'verbose_name': 'Vulnerability',
                'verbose_name_plural': 'Vulnerabilities',
            },
        ),
    ]
