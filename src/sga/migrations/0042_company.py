# Generated by Django 4.0.8 on 2022-11-23 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sga', '0041_alter_provider_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=50)),
                ('commercial_information', models.TextField()),
                ('logo', models.ImageField(upload_to='sga/logos')),
            ],
        ),
    ]
