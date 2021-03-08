# Generated by Django 2.2.13 on 2021-03-08 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('laboratory', '0021_auto_20210202_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Rols',
            },
        ),
        migrations.CreateModel(
            name='ProfilePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laboratories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratory.Laboratory', verbose_name='Laboratories')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratory.Profile', verbose_name='Profile')),
                ('rol', models.ManyToManyField(blank=True, to='laboratory.Rol', verbose_name='Rol')),
            ],
        ),
    ]
