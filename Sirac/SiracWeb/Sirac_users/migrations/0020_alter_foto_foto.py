# Generated by Django 3.2.3 on 2021-12-09 03:50

import Sirac_users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sirac_users', '0019_alter_foto_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='Foto',
            field=models.ImageField(upload_to=Sirac_users.models.cambiar_ruta_de_fichero, verbose_name='Foto'),
        ),
    ]