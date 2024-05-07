# Generated by Django 3.2.3 on 2021-12-08 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sirac_users', '0017_usuario_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='photo',
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo_foto', models.CharField(max_length=25, null=True, verbose_name='Titulo de foto')),
                ('Foto', models.FileField(upload_to='Fotos/', verbose_name='Foto')),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sirac_users.usuario', to_field='N_Documento', verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Foto',
                'verbose_name_plural': 'Fotos',
                'db_table': 'Foto',
                'ordering': ['id'],
            },
        ),
    ]