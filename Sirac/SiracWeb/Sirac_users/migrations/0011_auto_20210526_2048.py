# Generated by Django 3.0 on 2021-05-27 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sirac_users', '0010_auto_20210526_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='name_T_Document',
            field=models.CharField(max_length=40, verbose_name='Nombre tipo de Documento'),
        ),
    ]