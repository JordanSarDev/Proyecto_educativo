"""SiracWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from SiracWeb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name="index"),
    path('login/', views.Login),
    path('specialties/', views.Especialidades, name="specialties"),
    path('index/', views.Index),
    path('home/', views.Inicio, name="home"),
    path('home_appr/', views.Inicio_Aprendiz, name="home_appr"),
    path('home_ins/', views.Inicio_Instructor, name="home_ins"),
    path('list_stu/', views.Listado_Apre, name="list_stu"),
    path('login_admin/', views.Login_Admin),
    path('login_appr/', views.Login_Apre),
    path('login_ins/', views.Login_Ins),
    path('logout/', views.logout),
    path('profile_appr/', views.Perfil_Apre),
    path('profile_ins/', views.Perfil_Ins, name="profile_ins"),
    path('register_assis/', views.Registro_Asistencia, name="register_assis"), #Rol instructor
    path('take_assis/', views.Toma_Asistencia, name="take_assis"), #Rol instructor
    path('edit_assis/', views.Editar_Asistencia, name="edit_assis"), #Rol instructor
    path('see_assis/', views.Ver_Asistencia, name="see_assis"), #Rol aprendiz
    path('upload_file/', views.Subir_Excusa, name="upload_file"), #Rol aprendiz
    path('modify_appr/', views.Modificar_Apre),
    path('modify_ins/', views.Modifica_Ins),
    path('edit_appr/', views.Editar_Apre),
    path('edit_ficha/', views.Editar_Ficha),
    path('edit_ins/', views.Editar_Ins),
    path('edit_jorn/', views.Editar_Jornada),
    path('edit_doc/', views.Editar_Documento),
    path('edit_est/', views.Editar_Estado_de_Asistencia),
    path('edit_especialidad/', views.Editar_Especialidad),
    path('edit_sed/',views.Editar_Sede),
    path('edit_program/',views.Editar_Programa),
    path('edit_trimester/',views.Editar_Trimestre),
    path('edit_group/',views.Editar_Grupo),
    path('register_appr/', views.Registrar_Apre),
    path('register_new_ins/', views.Registrar_Ins),
    path('register_document/', views.Registro_Documento, name="register_document"),
    path('register_status/', views.Registro_Estado, name="register_status"),
    path('register_file/', views.Registro_Ficha, name="register_file"),
    path('register_group/', views.Registro_Grupo, name="register_group"),
    path('register_ins/', views.Registro_Instructor, name="register_ins"),
    path('register_jornada/', views.Registro_Jornada, name="register_jornada"),
    path('register_program/', views.Registro_Programa, name="register_program"),
    path('register_campus/', views.Registro_Sede, name="register_campus"),
    path('register_trimester/', views.Registro_Trimestre, name="register_trimester"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)