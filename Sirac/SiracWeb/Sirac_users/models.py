from django.db import models

from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.query import ValuesIterable
import os
import json

# Create your models here.

def cambiar_ruta_de_fichero(instance, filename):
    if os.path.isdir(os.path.join('media/Fotos/', instance.Titulo_foto)):
        pass
    else:
        os.mkdir(os.path.join('media/Fotos/', instance.Titulo_foto))
    return os.path.join('media/Fotos/', instance.Titulo_foto , filename)

class Documento(models.Model):
    name_T_Document = models.CharField(max_length=40, verbose_name="Nombre tipo de Documento")
    acronym_D = models.CharField(max_length=10, null=True, blank=True, verbose_name="Siglas de Documento")

    def __str__(self):
        return self.name_T_Document
    class Meta:
        verbose_name="Documento"
        verbose_name_plural = "Documentos"
        db_table = "Documento"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)


class Rol(models.Model):
    name_R = models.CharField(max_length=20, verbose_name="Nombre del Rol")

    def __str__(self):
        return self.name_R
    class Meta:
        verbose_name="Rol"
        verbose_name_plural = "Roles"
        db_table = "Rol"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)
    
class Trimestre(models.Model):
    name_Tri = models.CharField(max_length=20, verbose_name="Trimestre")

    def __str__(self):
        return self.name_Tri
    class Meta:
        verbose_name="Trimestre"
        verbose_name_plural = "Trimestres"
        db_table = "Trimestre"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Sede(models.Model):
    name_S = models.CharField(max_length=20,verbose_name="Nombre de Sede")
    address_S = models.CharField(max_length=30, null=True, blank=True, verbose_name="Dirección de Sede")
    city_S = models.CharField(max_length=20, verbose_name="Ciudad de Sede")
    
    def __str__(self):
        return self.name_S
    class Meta:
        verbose_name="Sede"
        verbose_name_plural = "Sedes"
        db_table = "Sede"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Programa(models.Model):
    name_P = models.CharField(max_length=50, verbose_name="Nombre de Programa")
    acronym_P= models.CharField(max_length=10, null=True, blank=True, verbose_name="Siglas del Programa")
     
    def __str__(self):
        return self.name_P
    class Meta:
        verbose_name="Programa"
        verbose_name_plural = "Programas"
        db_table = "Programa"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)
    
class Grupo(models.Model):
    Name_Group = models.CharField(max_length=30, verbose_name="Nombre Grupo")

    def __str__(self):
        return self.Name_Group
    class Meta:
        verbose_name="Grupo"
        verbose_name_plural = "Grupos"
        db_table = "Grupo"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)
    

class Jornada(models.Model):
    name_J = models.CharField(max_length=30, verbose_name= "Nombre Jornada")
    acronym_J = models.CharField(max_length=10, verbose_name= "Siglas Jornada")

    def __str__(self):
        return self.name_J
    class Meta:
        verbose_name="Jornada"
        verbose_name_plural = "Jornadas"
        db_table = "Jornada"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Estado_Asistencia(models.Model):
    name_E_Asis = models.CharField(max_length=20, verbose_name="Nombre Estado de Asistencia")

    def __str__(self):
        return self.name_E_Asis
    class Meta:
        verbose_name="Estado de Asistencia"
        verbose_name_plural = "Estados de Asistencia"
        db_table = "Estado de Asistencia"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

# Tablas debiles

class Adminitrador(models.Model):
    Username = models.CharField(max_length=10, verbose_name="Nombre de usuario")
    Password_Adm = models.CharField(max_length=25, verbose_name="Contraseña")
    Rol = models.ForeignKey(Rol, verbose_name="Rol", on_delete=models.CASCADE)

    def __str__(self):
        return self.Username
    class Meta:
        verbose_name="Administrador"
        verbose_name_plural = "Administradores"
        db_table = "Administrador"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Ficha(models.Model):
    number_F = models.CharField(unique=True, max_length=10, verbose_name="Numero de Ficha")
    Jornada = models.ForeignKey(Jornada, verbose_name="Jornada", on_delete=models.CASCADE)
    Sede = models.ForeignKey(Sede, verbose_name="Sede", on_delete= models.CASCADE)
    Programa = models.ForeignKey(Programa, verbose_name="Programa", on_delete= models.CASCADE)

    def __str__(self):
        return self.number_F
    class Meta:
        verbose_name="Ficha"
        verbose_name_plural = "Fichas"
        db_table = "Ficha"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Usuario(models.Model):
    N_Documento = models.CharField(max_length=25, unique=True, verbose_name="Numero de documento")
    first_name = models.CharField(max_length=40, verbose_name="Primer Nombre")
    second_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Segundo Nombre")
    F_last_name = models.CharField(max_length=45, verbose_name="Primer Apellido")
    S_last_name = models.CharField(max_length=45, null=True, blank=True, verbose_name="Segundo Apellido")
    Phone_number = models.CharField(max_length=15, verbose_name="Telefono Celular")
    Tel_number =models.CharField(max_length=40, null=True, blank=True, verbose_name="Telefono Fijo")
    Person_mail = models.CharField(max_length=45, null=True, blank=True, verbose_name="Correo Electronico Personal")
    Inst_mail = models.CharField(max_length=50, verbose_name="Correo Electronico Institucional")
    Date = models.CharField(max_length=30, null=True, verbose_name="Fecha de nacimiento")
    Documento = models.ForeignKey(Documento, verbose_name="Tipo de documento", on_delete=models.CASCADE)
    Rol = models.ForeignKey(Rol, verbose_name="Rol", on_delete=models.CASCADE)

    def __str__(self):
        return self.N_Documento
    class Meta:
        verbose_name="Usuario"
        verbose_name_plural = "Usuarios" 
        db_table = "Usuario"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Instructor(models.Model):
    N_Documento_I = models.ForeignKey(Usuario, to_field='N_Documento', verbose_name="Numero de Documento", on_delete=models.CASCADE)
    Password= models.CharField(max_length=25, verbose_name="Contraseña")

    def __str__(self):
        return str(self.N_Documento_I)   
    class Meta:
        verbose_name="Instructor"
        verbose_name_plural = "Instructores"
        db_table = "Instructor"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)
        

class Aprendiz(models.Model):
    N_Documento_A = models.ForeignKey(Usuario, to_field='N_Documento', related_name='NDocumentoA', verbose_name="Numero de documento", on_delete=models.CASCADE)
    Grupo = models.ForeignKey(Grupo, null=True, blank=True, verbose_name="Grupo", on_delete=models.CASCADE)
    Ficha = models.ForeignKey(Ficha, to_field='number_F', verbose_name="Numero de Ficha", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.N_Documento_A)
    class Meta:
        verbose_name="Aprendiz"
        verbose_name_plural = "Aprendices"
        db_table = "Aprendiz"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Especialidad(models.Model):
    name_E = models.CharField(max_length=50, verbose_name="Nombre Especialidad")
    Days_E = models.CharField(max_length=60, verbose_name="Dias Especialidad")
    Time_Begining = models.CharField(max_length=8, verbose_name="Hora de inico")
    Time_Ending = models.CharField(max_length=8, verbose_name="Hora final")
    Trimestre = models.ForeignKey(Trimestre, verbose_name="Trimestre", on_delete=models.CASCADE)
    Instructor = models.ForeignKey(Instructor, verbose_name="Instructor Encargado", on_delete=models.CASCADE)
    N_Ficha = models.ForeignKey(Ficha, verbose_name="Numero de Ficha", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name_E)
    class Meta:
        verbose_name="Especialidad"
        verbose_name_plural = "Especialidades"
        db_table = "Especialidad"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Asistencia(models.Model):
    Date_Asistencia = models.CharField(max_length=10, verbose_name="Fecha de Asistencia")
    Notes = models.CharField(max_length=70, null=True, blank=True, verbose_name="Anotaciones")
    Estado_Asistencia = models.ForeignKey(Estado_Asistencia, verbose_name="Estado de Asistencia", on_delete=models.CASCADE)
    Aprendiz = models.ForeignKey(Aprendiz, verbose_name="Aprendiz", on_delete=models.CASCADE)
    Especialidad = models.ForeignKey(Especialidad, verbose_name="Especialidad", on_delete=models.CASCADE)

    def __str__(self):
        return self.id
    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        db_table = "Asistencia"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class Excusa(models.Model):
    Name_Excusa = models.CharField(max_length=25, null=True, verbose_name="Nombre de Excusa")
    Date_Excusa = models.DateField(verbose_name="Fecha de Excusa", null=True)
    Soporte_Excusa = models.FileField(upload_to='Excusas/', verbose_name = "Soporte de la excusa")
    Description_Ex = models.CharField(max_length=50, null=True, blank=True, verbose_name="Descripcion Excusa")
    Asistencia = models.ForeignKey(Asistencia, verbose_name="Asistencia registrada", on_delete=models.CASCADE)

    def __str__(self):
        return self.Soporte_Excusa
    class Meta:
        verbose_name = "Excusa"
        verbose_name_plural = "Excusas"
        db_table = "Excusa"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)


class Foto(models.Model):
    Titulo_foto = models.CharField(max_length=25, null=True, verbose_name="Titulo de foto")
    Foto = models.ImageField(upload_to=cambiar_ruta_de_fichero, verbose_name = "Foto")
    Usuario = models.ForeignKey(Usuario, to_field='N_Documento', verbose_name="Usuario", on_delete=models.CASCADE)

    def __str__(self):
        return self.Titulo_foto
    class Meta:
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"
        db_table = "Foto"
        ordering = ["id"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)
