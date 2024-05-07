from django.contrib import admin

# Register your models here.
from Sirac_users.models import *

@admin.register(Adminitrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ("id", "Username")
    list_display_links = ("Username",)
    list_per_page = 10

@admin.register(Aprendiz)
class AprendizAdmin(admin.ModelAdmin):
    list_display = ("id", "N_Documento_A", "Ficha", "Grupo")
    list_display_links = ("N_Documento_A",)
    search_fields = ("N_Documento_A",)
    list_filter = ("Ficha",)
    list_per_page = 10

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "Date_Asistencia", "Aprendiz", "Especialidad", "Estado_Asistencia", "Notes")
    list_display_links = ("Date_Asistencia",) 
    list_editable = ("Notes", "Estado_Asistencia") 
    search_fields = ("Aprendiz",)  
    list_filter = ("Date_Asistencia",)
    list_per_page = 10

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("id", "name_T_Document", "acronym_D")
    list_display_links = ("name_T_Document",)
    list_editable = ("acronym_D",) 
    list_per_page = 5 

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("id", "name_E", "N_Ficha", "Trimestre", "Instructor", "Days_E", "Time_Begining", "Time_Ending")  
    list_display_links = ("name_E",)
    list_editable =("N_Ficha", "Trimestre", "Instructor", "Days_E", "Time_Begining", "Time_Ending")
    search_fields = ("name_E",)
    list_filter = ("N_Ficha", "Instructor", "Trimestre",)
    list_per_page = 10
    
@admin.register(Estado_Asistencia)
class Estado_AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "name_E_Asis")
    list_display_links = ("name_E_Asis",)
    list_per_page = 10

@admin.register(Excusa)
class ExcusaAdmin(admin.ModelAdmin):
    list_display = ("id", "Date_Excusa", "Asistencia", "Name_Excusa", "Soporte_Excusa", "Description_Ex")
    list_display_links = ("Date_Excusa",)
    list_editable =("Description_Ex", "Name_Excusa") 
    search_fields = ("Asistencia",) 
    list_filter = ("Date_Excusa",)
    list_per_page = 10 

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ("id", "Titulo_foto", "Foto", "Usuario")
    list_display_links = ("Foto",)
    list_editable =("Titulo_foto",) 
    search_fields = ("Usuario",) 
    list_filter = ("Titulo_foto",)
    list_per_page = 10 

@admin.register(Ficha)
class FichaAdmin(admin.ModelAdmin):
    list_display = ("id", "number_F", "Programa", "Sede", "Jornada")
    list_display_links = ("number_F",)
    llist_editable =("Sede",)
    search_fields = ("number_F",)
    list_filter = ("Programa",)
    list_per_page = 10

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ("id", "Name_Group")
    list_display_links = ("Name_Group",)
    list_per_page = 10

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("id", "N_Documento_I")
    list_display_links = ("N_Documento_I",)
    search_fields = ("N_Documento_I",)
    list_per_page = 10

@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):
    list_display = ("id", "name_J", "acronym_J")
    list_display_links = ("name_J",)
    list_editable = ("acronym_J",)
    list_per_page = 5
    
@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ("id", "name_P", "acronym_P")
    list_display_links = ("name_P",)
    list_editable =("acronym_P",)
    search_fields = ("name_P",)
    list_per_page = 5
    
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "name_R")
    list_display_links = ("name_R",)
    list_per_page = 5
    
@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ("id", "name_S", "city_S", "address_S")
    list_display_links = ("name_S",)
    llist_editable = ("address_S",)
    search_fields = ("name_S",)
    list_filter = ("city_S",)
    list_per_page = 5    
    
@admin.register(Trimestre)
class TrimestreAdmin(admin.ModelAdmin):
    list_display = ("id", "name_Tri")
    list_display_links = ("name_Tri",)
    list_per_page = 5
    
@admin.register(Usuario)   
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "second_name", "F_last_name", "S_last_name", "N_Documento", "Documento", "Rol", "Inst_mail", "Person_mail", "Phone_number", "Tel_number", "Date")
    list_display_links = ("first_name","second_name","F_last_name","S_last_name")
    list_editable = ("Person_mail", "Tel_number", "Date")
    search_fields = ("first_name", "second_name", "F_last_name", "S_last_name", "N_Documento")  
    list_filter = ("Documento", "Rol")
    list_per_page = 10