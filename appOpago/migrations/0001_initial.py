# Generated by Django 4.1 on 2023-08-19 03:48

import appOpago.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Area',
            },
        ),
        migrations.CreateModel(
            name='concepto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('monto', models.CharField(default=0, max_length=10)),
                ('area', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='appOpago.area')),
            ],
        ),
        migrations.CreateModel(
            name='productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ordenes_pago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('folio', models.CharField(default=appOpago.models.clave, max_length=50)),
                ('fecha_emision', models.DateField(default=datetime.datetime.now)),
                ('nombre_solicitante', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('estatus', models.BooleanField(default=False)),
                ('producto', models.FileField(blank=True, null=True, upload_to='media/')),
                ('monto', models.FloatField(default=0)),
                ('area', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='appOpago.area')),
                ('concepto', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='appOpago.concepto')),
            ],
        ),
    ]
