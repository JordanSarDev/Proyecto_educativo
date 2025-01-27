# Generated by Django 3.2.3 on 2021-12-08 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sirac_users', '0015_alter_usuario_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='photo',
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='Date_Asistencia',
            field=models.CharField(max_length=10, verbose_name='Fecha de Asistencia'),
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='Time_Begining',
            field=models.CharField(max_length=8, verbose_name='Hora de inico'),
        ),
        migrations.AlterField(
            model_name='especialidad',
            name='Time_Ending',
            field=models.CharField(max_length=8, verbose_name='Hora final'),
        ),
        migrations.AlterField(
            model_name='excusa',
            name='Date_Excusa',
            field=models.DateField(null=True, verbose_name='Fecha de Excusa'),
        ),
        migrations.AlterField(
            model_name='excusa',
            name='Name_Excusa',
            field=models.CharField(max_length=25, null=True, verbose_name='Nombre de Excusa'),
        ),
        migrations.AlterField(
            model_name='excusa',
            name='Soporte_Excusa',
            field=models.FileField(upload_to='Excusas/', verbose_name='Soporte de la excusa'),
        ),
    ]
