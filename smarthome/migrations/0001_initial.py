# Generated by Django 3.1.4 on 2021-01-29 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to='Device')),
                ('release_date', models.DateField()),
                ('manufacturer_name', models.CharField(max_length=200)),
                ('connector', models.CharField(max_length=20)),
                ('generation', models.CharField(max_length=10)),
                ('category', models.CharField(choices=[('SL', 'SMART_LIGHTING'), ('SLO', 'SMART_LOCK'), ('SMW', 'SMART_METERING_WATER'), ('SME', 'SMART_METERING_ELECTRICITY'), ('SMWA', 'SMAERT_METERING_WARMTH'), ('VA', 'VIRTUAL_ASSISTANT'), ('ST', 'SMART_THERMOSTAT'), ('SC', 'SMART_CAM'), ('SSS', 'SMART_SECURITY_SYSTEM')], max_length=4)),
            ],
            options={
                'verbose_name': 'Gerät',
                'verbose_name_plural': 'Geräte',
            },
        ),
        migrations.CreateModel(
            name='DeviceEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Firmware',
            fields=[
                ('firmware_id', models.AutoField(primary_key=True, serialize=False)),
                ('version_number', models.CharField(max_length=50, verbose_name='Versionsnummer')),
                ('changelog', models.CharField(max_length=500, verbose_name='Änderungen')),
                ('changelog_en', models.CharField(max_length=500, null=True, verbose_name='Änderungen')),
                ('changelog_de', models.CharField(max_length=500, null=True, verbose_name='Änderungen')),
                ('release_date', models.DateField(verbose_name='Erscheinungsdatum')),
            ],
            options={
                'verbose_name': 'Firmware',
                'verbose_name_plural': 'Firmwares',
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connector', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discovered_date', models.DateField(verbose_name='Schwachstelle wurde gefunden am:')),
                ('description', models.CharField(max_length=300, verbose_name='Beschreibung der Schwachstelle')),
                ('url', models.URLField(verbose_name='URL zum Artikel der Schwachstelle')),
                ('category', models.CharField(max_length=20, verbose_name='Kategorie')),
                ('patch_date', models.DateField(verbose_name='Schwachstelle wurde gepatched am:')),
                ('url_patch', models.URLField(verbose_name='Link zum Artikel des Patches')),
                ('patched', models.BooleanField(default=False, verbose_name='Schwachstelle wurde behoben:')),
                ('device_id', models.ManyToManyField(to='smarthome.Device', verbose_name='Schwachstelle bei folgenden Geräten ausnutzbar:')),
            ],
            options={
                'verbose_name': 'Schwachstelle',
                'verbose_name_plural': 'Schwachstellen',
            },
        ),
    ]
