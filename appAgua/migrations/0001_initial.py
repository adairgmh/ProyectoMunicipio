# Generated by Django 4.1 on 2023-08-19 03:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cobrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Colonia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_colonia', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Comunidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_comunidad', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_concepto', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Predio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claveCatastral', models.CharField(max_length=31, unique=True)),
                ('cp', models.CharField(max_length=45)),
                ('calle', models.CharField(max_length=45)),
                ('numeroext', models.CharField(max_length=45)),
                ('numeroint', models.CharField(max_length=45)),
                ('colonia', models.CharField(max_length=45)),
                ('ciudad', models.CharField(max_length=45)),
                ('estado', models.CharField(max_length=45)),
                ('tipo', models.CharField(max_length=12)),
                ('rfc', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_propietario', models.CharField(max_length=45)),
                ('apellido_paterno', models.CharField(max_length=45)),
                ('apellido_materno', models.CharField(max_length=45)),
                ('genero', models.CharField(max_length=15)),
                ('calle', models.CharField(max_length=45)),
                ('numero_celular', models.CharField(max_length=10)),
                ('codigo_postal', models.IntegerField()),
                ('municipio', models.CharField(max_length=45)),
                ('estado', models.CharField(default='Tlaxcala', max_length=45)),
                ('email', models.CharField(max_length=45)),
                ('colonia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.colonia')),
                ('comunidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.comunidad')),
            ],
        ),
        migrations.CreateModel(
            name='Tipos_servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave_tipo_servicio', models.CharField(max_length=45)),
                ('tipo_uso_de_servicio', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_servicio', models.CharField(max_length=10, unique=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('costo', models.FloatField()),
                ('id_colonia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.colonia')),
                ('id_comunidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.comunidad')),
                ('id_propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.propietario')),
                ('id_tipos_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.tipos_servicio')),
                ('no_predio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.predio')),
            ],
        ),
        migrations.CreateModel(
            name='Pagos_anuales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_servicio', models.IntegerField()),
                ('anio', models.IntegerField()),
                ('fecha', models.DateField()),
                ('monto_mensual', models.FloatField()),
                ('descuento', models.FloatField()),
                ('multa', models.CharField(max_length=45)),
                ('id_colonia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.colonia')),
                ('id_comunidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.comunidad')),
                ('id_propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.propietario')),
                ('id_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_servicio', models.CharField(max_length=10, unique=True)),
                ('fecha_pago', models.DateField(default=datetime.datetime.now)),
                ('costo', models.FloatField(default=0.0)),
                ('descuento', models.FloatField(default=0.0)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('mes', multiselectfield.db.fields.MultiSelectField(choices=[('Enero', 'Enero'), ('Febrero', 'Febrero'), ('Marzo', 'Marzo'), ('Abril', 'Abril'), ('Mayo', 'Mayo'), ('Junio', 'Junio'), ('Julio', 'Julio'), ('Agosto', 'Agosto'), ('Septiembre', 'Septiembre'), ('Octubre', 'Octubre'), ('Noviembre', 'Noviembre'), ('Diciembre', 'Diciembre')], max_length=15)),
                ('anio', models.IntegerField(default=0)),
                ('multa', models.IntegerField(default=0)),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.concepto')),
                ('id_cobrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.cobrador')),
                ('id_colonia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.colonia')),
                ('id_comunidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.comunidad')),
                ('id_propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.propietario')),
                ('id_tipos_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAgua.tipos_servicio')),
            ],
        ),
    ]
