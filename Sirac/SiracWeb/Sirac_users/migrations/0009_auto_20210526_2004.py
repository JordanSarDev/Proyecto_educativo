# Generated by Django 3.0 on 2021-05-27 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sirac_users', '0008_excusa_soporte_excusa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprendiz',
            name='Grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sirac_users.Grupo', verbose_name='Grupo'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='Notes',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Anotaciones'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='acronym_D',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Siglas de Documento'),
        ),
        migrations.AlterField(
            model_name='excusa',
            name='Description_Ex',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Descripcion Excusa'),
        ),
        migrations.AlterField(
            model_name='programa',
            name='acronym_P',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Siglas del Programa'),
        ),
        migrations.AlterField(
            model_name='sede',
            name='adress_S',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Dirección de Sede'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='Person_mail',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Correo Electronico Personal'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='S_last_name',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Segundo Apellido'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='Tel_number',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Telefono Fijo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='second_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Segundo Nombre'),
        ),
    ]