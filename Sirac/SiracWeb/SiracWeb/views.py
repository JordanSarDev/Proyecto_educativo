from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.views.static import serve
from Sirac_users.models import *
import datetime
import os
import json

# METODOS


def main(request):
    request.session['login'] = 0


def authenticate(request, url):
    if request.session['login'] == 1:
        return render(request, "Administrador/Inicio_Administrador.html", {
        })
    elif request.session['login'] == 2:
        return Inicio_Instructor(request)
    elif request.session['login'] == 3:
        return Inicio_Aprendiz(request)
    else:
        return render(request, url, {})


def authenticate_appr(request, url, cxt):
    if request.session['login'] == 1:
        return render(request, "Administrador/Inicio_Administrador.html", {
        })
    elif request.session['login'] == 2:
        return render(request, "Instructor/Inicio_Instructor.html", request.session['instru'])
    elif request.session['login'] == 3:
        if cxt == {}:
            return render(request, url, request.session['appr'])
        else:
            return render(request, url, cxt)
    else:
        return render(request, "Login/Login.html", {})


def authenticate_instru(request, url, ins):
    if request.session['login'] == 1:
        return render(request, "Administrador/Inicio_Administrador.html", {
        })
    elif request.session['login'] == 2:
        if ins == {}:
            return render(request, url, request.session['instru'])
        else:
            return render(request, url, ins)
    elif request.session['login'] == 3:
        return render(request, "Aprendiz/Inicio_Aprendiz.html", request.session['appr'])
    else:
        return render(request, "Login/Login.html", {})


def authenticate_admin(request, url, ctx):
    if 'login' in request.session:
        if request.session['login'] == 1:
            return render(request, url, ctx)
        elif request.session['login'] == 2:
            return render(request, "Instructor/Inicio_Instructor.html", request.session['instru'])
        elif request.session['login'] == 3:
            return render(request, "Aprendiz/Inicio_Aprendiz.html", request.session['appr'])
    else:
        return render(request, "Login/Login.html", {})


def logout(request):
    request.session.flush()
    return redirect('/index/')


def filtrar_listado(request):
    ficha = request.session['ficha']
    if 'ficha' in request.session:
        aprendices = list(Aprendiz.objects.all().filter(Ficha_id=ficha['number_F']))
        return aprendices
    else:
        return authenticate(request, "")


def aprendiz_especialidades(request):
    especialidades = list(Especialidad.objects.all().filter(N_Ficha_id=request.session['ficha']))
    especialidades_t = {}
    id = 1
    for dato in especialidades:
        especialidad = json.loads(Especialidad.objects.get(id=dato.id).toJSON())
        especialidades_t['esp_' + str(id)] = especialidad
        id = id+1
    return especialidades_t

def obtener_especialidades(request):
    especialidades = list(Especialidad.objects.all().filter(Instructor_id=request.session['instru'].get('id')))
    especialidades_t = {}
    fichas_t = {}
    id = 1
    for dato in especialidades:
        especialidad = json.loads(Especialidad.objects.get(id=dato.id).toJSON())
        especialidad['ficha'] = json.loads(Ficha.objects.get(id=dato.N_Ficha_id).toJSON())
        fichas_t['ficha_'+str(id)] = especialidad['ficha']
        especialidades_t['esp_' + str(id)] = especialidad
        id = id+1
    return {'especialidades':especialidades_t, 'fichas':fichas_t}

def obtener_meses():
    meses = {'Enero':'1', 'Febrero':'2', 'Marzo':'3', 'Abril':'4','Mayo':'5',
             'Junio':'6', 'Julio':'7', 'Agosto':'8', 'Septiembre':'9', 
             'Octubre':'10', 'Noviembre':'11', 'Diciembre':'12'}
    return meses

def obtener_fecha_actual():
    fecha = {'texto':datetime.datetime.now().date, 'numero':
             str(datetime.datetime.now().year) + "-" + 
             str(datetime.datetime.now().month) + "-" + 
             str(datetime.datetime.now().day)}
    return fecha

# LOGIN


def Index(request):
    if 'login' not in request.session:
        main(request)
    return authenticate(request, "index.html")


def Login(request):
    if 'login' not in request.session:
        main(request)
    return authenticate(request, "Login/Login.html")


def Login_Admin(request):
    if 'login' not in request.session:
        main(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != None and password != None:
            if Adminitrador.objects.filter(Username=username, Password_Adm=password).exists():
                admin = Adminitrador.objects.get(Username=username)
                request.session['admin'] = admin.toJSON()
                request.session['login'] = 1
                return redirect('/home/')
            else:
                messages.error(request, 'Usuario o Contraseña incorrecta')
    return authenticate(request, "Login/Login_Administrador.html")

def Login_Apre(request):
    if 'login' not in request.session:
        main(request)
    if request.method == 'POST':
        N_Documento = request.POST.get('N_Documento')
        if N_Documento != None:
            if Aprendiz.objects.filter(N_Documento_A=N_Documento).exists():
                appr = json.loads(Usuario.objects.get(N_Documento=N_Documento).toJSON())
                appr['id'] = json.loads(Aprendiz.objects.get(N_Documento_A_id=N_Documento).toJSON()).get('id')
                ficha = json.loads(Aprendiz.objects.get(N_Documento_A_id=N_Documento).toJSON()).get('Ficha_id')
                appr['ficha'] = json.loads(Ficha.objects.get(number_F=ficha).toJSON()).get('id')
                request.session['ficha'] = appr['ficha']
                request.session['appr'] = appr
                request.session['login'] = 3
                return redirect('/home_appr/') 
            else:
                messages.error(request, 'Numero de documento incorrecto')
    return authenticate(request, "Login/Login_Aprendiz.html")


def Login_Ins(request):
    if 'login' not in request.session:
        main(request)
    if request.method == 'POST':
        N_Documento = request.POST.get('N_Documento')
        password = request.POST.get('password')
        if N_Documento != None and password != None:
            if Instructor.objects.filter(N_Documento_I_id=N_Documento, Password=password).exists():
                instru = json.loads(Usuario.objects.get(N_Documento=N_Documento).toJSON())
                instru['id'] = json.loads(Instructor.objects.get(N_Documento_I_id=N_Documento).toJSON()).get('id')
                request.session['instru'] = instru
                request.session['login'] = 2
                return redirect('/home_ins/')
            else:
                messages.error(
                    request, 'Numero de documento o Contraseña incorrecta')
    return authenticate(request, "Login/Login_Instructor.html")


def Inicio(request):
    return authenticate(request, "Login.html")

# MODULO APRENDIZ

def Inicio_Aprendiz(request): 
    cxt = request.session['appr']
    cxt['especialidades_t'] = aprendiz_especialidades(request)
    if request.method == 'POST':
        especialidad = request.POST.get('especialidad')
        if especialidad != None and especialidad != "":
            request.session['especialidad'] = json.loads(Especialidad.objects.get(id=especialidad).toJSON())
            return redirect('/see_assis/')
    return authenticate_appr(request, "Aprendiz/Inicio_Aprendiz.html", cxt)

def Perfil_Apre(request):
    cxt = request.session['appr']
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt['documentos_t'] = documentos_t
    cxt['especialidades_t'] = aprendiz_especialidades(request)
    if Foto.objects.filter(Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento'])).exists():
        cxt['foto'] = json.loads(Foto.objects.get(Usuario=cxt['N_Documento']).toJSON())
    if request.method == 'POST':
        especialidad = request.POST.get('especialidad')
        if especialidad != None and especialidad != "":
            request.session['especialidad'] = json.loads(Especialidad.objects.get(id=especialidad).toJSON())
            return redirect('/see_assis/')
        subir_foto = request.POST.get('subir_foto')
        if subir_foto == "100":
            foto = request.FILES['foto']
            if foto != None and foto != "":
                if Foto.objects.filter(Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento'])).exists():
                    Foto.objects.filter(Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento'])).delete()
                Foto.objects.create(Titulo_foto=cxt['first_name']+"_"+cxt['F_last_name'], Foto=foto, Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento']))
                return redirect('/profile_appr/')
    return authenticate_appr(request, "Aprendiz/Perfil_Aprendiz.html", cxt)

def Modificar_Apre(request):
    appr = request.session['appr']
    appr['especialidades_t'] = aprendiz_especialidades(request)
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    appr['documentos_t'] = documentos_t
    appr['especialidades_t'] = aprendiz_especialidades(request)
    if request.method == 'POST':
        especialidad = request.POST.get('especialidad')
        if especialidad != None and especialidad != "":
            request.session['especialidad'] = json.loads(Especialidad.objects.get(id=especialidad).toJSON())
            return redirect('/see_assis/')
        if request.POST.get('Aceptar') == 'Si':
            Phone_number = request.POST.get('Phone_number')
            Tel_number = request.POST.get('Tel_number')
            Person_mail = request.POST.get('Person_mail')
            if Phone_number != None and Phone_number != "":
                Usuario.objects.filter(N_Documento=appr['N_Documento']).update(
                    Phone_number = Phone_number, Tel_number = Tel_number, Person_mail = Person_mail)
                appr = json.loads(Usuario.objects.get(N_Documento=appr['N_Documento']).toJSON())
                appr['id'] = json.loads(Aprendiz.objects.get(N_Documento_A_id=appr['N_Documento']).toJSON()).get('id')
                request.session['appr'] = appr
                return redirect('/profile_appr/') 
    return authenticate_appr(request, "Aprendiz/Modificar_Aprendiz.html", {})

def Ver_Asistencia(request):
    aprendiz = request.session['appr']
    especialidad = request.session['especialidad']
    asistencias = list(Asistencia.objects.filter(Aprendiz_id=aprendiz['id'], Especialidad_id=especialidad['id']))
    instructor = json.loads(Instructor.objects.get(id=request.session['especialidad'].get('Instructor_id')).toJSON()).get('N_Documento_I_id')
    estados = list(Estado_Asistencia.objects.all())
    estados_t = {}
    aprendiz = {}
    asistencias_t = {}
    conteo = {'si':0, 'no':0}
    id = 1
    for est in estados:
        estados_t['est_' + str(id)] = json.loads(Estado_Asistencia.objects.get(id=est.id).toJSON())
        id = id+1
    id = 1
    for asis in asistencias:
        asistencia = json.loads(Asistencia.objects.get(id=asis.id).toJSON())
        dia = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[8:]
        mes = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[5:7]
        año = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[:4]
        asistencia['fecha'] = {'dia':dia, 'mes':mes, 'año':año}
        if Excusa.objects.filter(Asistencia_id=asistencia['id']).exists():
            asistencia['excusa'] = json.loads(Excusa.objects.get(Asistencia_id=asistencia['id']).toJSON()).get('Soporte_Excusa')
        else:
            asistencia['excusa'] = ""
        asistencias_t['asis_' + str(id)] = asistencia
        if asistencias_t['asis_' + str(id)].get('Estado_Asistencia_id') == 1:
            conteo['si'] = conteo['si']+1
        else:
            conteo['no'] = conteo['no']+1
        id = id+1
    aprendiz['meses'] = obtener_meses()
    aprendiz['conteo'] = conteo
    aprendiz['estados_t'] = estados_t
    aprendiz['asistencias_t'] = asistencias_t
    aprendiz['especialidad'] = especialidad
    aprendiz['especialidades_t'] = aprendiz_especialidades(request)
    aprendiz['instructor'] = json.loads(Usuario.objects.get(N_Documento=instructor).toJSON())
    if request.method == 'POST':
        especialidad = request.POST.get('especialidad')
        if especialidad != None and especialidad != "":
            request.session['especialidad'] = json.loads(Especialidad.objects.get(id=especialidad).toJSON())
            return redirect('/see_assis/')
        asistencia = request.POST.get('asistencia')
        if asistencia != None and asistencia != "":
            request.session['asistencia'] = json.loads(Asistencia.objects.get(id=asistencia).toJSON())
            return redirect('/upload_file/')
        excusa = request.POST.get('excusa')
        if excusa != None and excusa != "":
            return serve(request, os.path.basename(excusa), os.path.dirname(excusa))
        seleccion_mes = request.POST.get('mes_seleccionado')
        if seleccion_mes != None and seleccion_mes != "":
            request.session['mes_seleccionado'] = seleccion_mes
    if 'mes_seleccionado' not in request.session:
        aprendiz['mes_seleccionado'] = obtener_fecha_actual().get('numero')[5:7]
    else:
        aprendiz['mes_seleccionado'] = request.session['mes_seleccionado']
    return authenticate_appr(request, "Aprendiz/Ver_Asistencias.html", aprendiz)

def Subir_Excusa(request):
    cxt = {}
    asistencia = request.session['asistencia']
    ficha = json.loads(Ficha.objects.get(id=request.session['especialidad'].get('N_Ficha_id')).toJSON()).get('number_F')
    cxt['especialidad'] = request.session['especialidad']
    cxt['ficha'] = ficha
    if request.method == 'POST':
        excusa = request.FILES['excusa']
        print(excusa)
        if excusa != None and excusa != "":
            Excusa.objects.create(Asistencia_id=asistencia['id'], Soporte_Excusa=excusa)
            return redirect('/see_assis/')
    return authenticate_appr(request, "Aprendiz/Subir_Excusa.html", cxt)

# MODULO INSTRUCTOR

def Inicio_Instructor(request): 
    programas = list(Programa.objects.all())
    programas_t = {}
    cxt = {}
    id = 1
    for dato in programas:
        programas_t['doc_' + str(id)] = json.loads(Programa.objects.get(name_P=dato.name_P).toJSON())
        id = id+1
    request.session['fichas'] = obtener_especialidades(request).get('fichas')
    cxt['especialidades_t'] = obtener_especialidades(request).get('especialidades')
    cxt['programas_t'] = programas_t
    if request.method == 'POST':
        registro = request.POST.get('registro')
        toma = request.POST.get('toma')
        especialidad = request.POST.get('especialidad')
        if registro != None and registro != "":
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=registro).toJSON())
            request.session['especialidad'] = especialidad
            return redirect('/register_assis/')
        if toma != None and toma != "":
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=toma).toJSON())
            request.session['especialidad'] = especialidad
            return redirect('/take_assis/')
    return authenticate_instru(request, "Instructor/Inicio_Instructor.html", cxt)

def Perfil_Ins(request):
    cxt = request.session['instru']
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt['especialidades_t'] = obtener_especialidades(request).get('especialidades')
    cxt['documentos_t'] = documentos_t
    if Foto.objects.filter(Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento'])).exists():
        cxt['foto'] = json.loads(Foto.objects.get(Usuario=cxt['N_Documento']).toJSON())
    if request.method == 'POST':
        ficha = request.POST.get('ficha')
        if ficha != None and ficha != "":
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=ficha).toJSON())
            return redirect('/register_assis/')
        subir_foto = request.POST.get('subir_foto')
        if subir_foto == "100":
            foto = request.FILES['foto']
            if foto != None and foto != "":
                if Foto.objects.filter(Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento'])).exists():
                    Foto.objects.filter(Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento'])).delete()
                Foto.objects.create(Titulo_foto=cxt['first_name']+"_"+cxt['F_last_name'], Foto=foto, Usuario=Usuario.objects.get(N_Documento=cxt['N_Documento']))
                return redirect('/profile_appr/')
        old_psw = request.POST.get('old_psw')
        new_psw = request.POST.get('new_psw')
        confirm_psw = request.POST.get('confirm_psw')
        ficha = request.POST.get('ficha')
        if old_psw != None and new_psw != None and new_psw != "" and confirm_psw != None and confirm_psw != "":
            password = json.loads(Instructor.objects.get(N_Documento_I_id=request.session['instru'].get('N_Documento')).toJSON()).get('Password')
            if old_psw == password:
                if new_psw == confirm_psw:
                    Instructor.objects.filter(N_Documento_I_id=request.session['instru'].get('N_Documento')).update(Password=new_psw)
                    messages.error(request, 'Se ha actualizado la contraseña correctamente')
                else:
                    messages.error(request, '¡ERROR! Las contraseñas no coinciden')
            else:
                messages.error(request, '¡ERROR! La contraseña antigua ingresada es incorrecta')
        else:
            messages.error(request, '¡ERROR! Debes ingresar los datos requeridos')
    return authenticate_instru(request, "Instructor/Perfil_Instructor.html", cxt)


def Modifica_Ins(request):
    ins = request.session['instru']
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    ins['documentos_t'] = documentos_t
    ins['especialidades_t'] = obtener_especialidades(request).get('especialidades')
    if request.method == 'POST':
        ficha = request.POST.get('ficha')
        if ficha != None and ficha != "":
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=ficha).toJSON())
            return redirect('/register_assis/')
        if request.POST.get('Aceptar') != 'Si':
            Phone_number = request.POST.get('Phone_number')
            Tel_number = request.POST.get('Tel_number')
            Person_mail = request.POST.get('Person_mail')
            if Phone_number != None and Phone_number != "":
                Usuario.objects.filter(N_Documento=ins['N_Documento']).update(
                    Phone_number = Phone_number, Tel_number = Tel_number, Person_mail = Person_mail)
                instru = json.loads(Usuario.objects.get(N_Documento=ins['N_Documento']).toJSON())
                instru['id'] = json.loads(Instructor.objects.get(N_Documento_I_id=ins['N_Documento']).toJSON()).get('id')
                request.session['instru'] = instru
                return redirect('/profile_ins/')
    return authenticate_instru(request, "Instructor/Modificar_Instructor.html", ins)

def Toma_Asistencia(request):
    cxt = {}
    cxt['fecha'] = obtener_fecha_actual()
    especialidad = request.session['especialidad']
    print(especialidad)
    if request.method == 'POST':
        ficha = request.POST.get('ficha')
        if ficha != None and ficha != "":
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=ficha).toJSON())
            return redirect('/register_assis/')
        Notes = request.POST.get('Notes')
        Aprendiz_id = request.POST.get('Aprendiz_id')
        estado = request.POST.get('estado')
        fecha = cxt['fecha'].get('numero')
        if estado != "" and estado != None:
            if not(Asistencia.objects.filter(Date_Asistencia=fecha, Aprendiz_id=Aprendiz_id, Especialidad_id=especialidad).exists()):
                newAsist = Asistencia(Date_Asistencia=fecha, Notes=Notes, Aprendiz_id=Aprendiz_id, Especialidad_id=especialidad, Estado_Asistencia_id=estado)
                newAsist.save()
            else:
                Asistencia.objects.filter(Date_Asistencia=fecha, Aprendiz_id=Aprendiz_id, Especialidad_id=especialidad).update(Estado_Asistencia_id=estado, Notes=Notes)
    aprendices = filtrar_listado(request)
    aprendiz = {}
    tabla = {}
    id = 1
    for dato in aprendices:
        aprendiz = json.loads(Usuario.objects.get(N_Documento=dato.N_Documento_A_id).toJSON())
        aprendiz['num'] = id
        aprendiz['id'] = json.loads(Aprendiz.objects.get(N_Documento_A_id=dato.N_Documento_A_id).toJSON()).get('id')
        if Asistencia.objects.filter(Aprendiz_id=aprendiz['id'], Date_Asistencia=cxt['fecha'].get('numero'), Especialidad_id=especialidad).exists():
            aprendiz['asis'] = json.loads(Asistencia.objects.get(Aprendiz_id=aprendiz['id'], Date_Asistencia=cxt['fecha'].get('numero'), Especialidad_id=especialidad).toJSON())
        else:
            aprendiz['asis'] = {'Estado_Asistencia_id':0}
        tabla['appr_' + str(id)] = aprendiz
        id = id+1
    cxt['tabla'] = tabla
    ficha = request.session['ficha']
    ficha['programa'] = json.loads(Programa.objects.get(id=ficha['Programa_id']).toJSON()).get('name_P')
    ficha['especialidad'] = especialidad
    cxt['especialidades_t'] = obtener_especialidades(request).get('especialidades')
    cxt['ficha'] = ficha
    return authenticate_instru(request, "Instructor/Tomar_Asistencia.html", cxt)

def Registro_Asistencia(request):
    aprendices = filtrar_listado(request)
    aprendiz = {}
    tabla = {}
    id = 1
    for dato in aprendices:
        aprendiz = json.loads(Usuario.objects.get(N_Documento=dato.N_Documento_A_id).toJSON())
        aprendiz['num'] = id
        aprendiz['id'] = json.loads(Aprendiz.objects.get(N_Documento_A_id=dato.N_Documento_A_id).toJSON()).get('id')
        asistencias = list(Asistencia.objects.filter(Aprendiz_id=aprendiz['id'], Especialidad_id=request.session['especialidad']))
        asistencia = {}
        excusas = {}
        num = 1
        conteo = {'si':0, 'no':0}
        for asis in asistencias:
            asistencia_t = json.loads(Asistencia.objects.get(id=asis.id).toJSON())
            dia = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[8:]
            mes = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[5:7]
            año = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[:4]
            asistencia_t['fecha'] = {'dia':dia, 'mes':mes, 'año':año}
            asistencia['asis_' + str(num)] = asistencia_t
            if asistencia['asis_' + str(num)].get('Estado_Asistencia_id') == 1:
                conteo['si'] = conteo['si']+1
            else:
                conteo['no'] = conteo['no']+1
                if asistencia['asis_' + str(num)].get('Estado_Asistencia_id') == 3:
                    if Excusa.objects.filter(Asistencia_id=asistencia['asis_' + str(num)].get('id')).exists():
                        excusas['exc_'+str(num)] = json.loads(Excusa.objects.get(Asistencia_id=asistencia['asis_' + str(num)].get('id')).toJSON())
                    else:
                        excusas['exc_'+str(num)] = {'Asistencia_id':asistencia['asis_' + str(num)].get('id'), 'Soporte_Excusa':'no'}
            num = num+1
        aprendiz['conteo'] = conteo
        aprendiz['asistencias'] = asistencia
        aprendiz['excusas'] = excusas
        tabla['appr_' + str(id)] = aprendiz
        id = id+1
    asistencias = list(Asistencia.objects.filter(Aprendiz_id=aprendiz['id'], Especialidad_id=request.session['especialidad']))
    fechas = {}
    num = 1
    for asistencia in asistencias:
        dia = json.loads(Asistencia.objects.get(id=asistencia.id).toJSON()).get('Date_Asistencia')[8:]
        mes = json.loads(Asistencia.objects.get(id=asistencia.id).toJSON()).get('Date_Asistencia')[5:7]
        fechas['fecha_' + str(num)] = {'dia':dia, 'mes':mes}
        num = num+1
    cxt = {'tabla': tabla}
    cxt['fechas'] = fechas
    ficha = request.session['ficha']
    ficha['programa'] = json.loads(Programa.objects.get(id=ficha['Programa_id']).toJSON()).get('name_P')
    especialidad = json.loads(Especialidad.objects.get(id=request.session['especialidad']).toJSON()).get('name_E')
    ficha['especialidad'] = especialidad
    cxt['meses'] = obtener_meses()
    cxt['ficha'] = ficha
    cxt['especialidades_t'] = obtener_especialidades(request).get('especialidades')
    cxt['fecha'] = datetime.datetime.now().date
    if request.method == 'POST':
        ficha = request.POST.get('ficha')
        especialidad = request.POST.get('especialidad')
        if ficha != None and ficha != "":
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=ficha).toJSON())
            request.session['especialidad'] = especialidad
            return redirect('/register_assis/')
        excusa = request.POST.get('excusa')
        if excusa != None and excusa != "":
            return serve(request, os.path.basename(excusa), os.path.dirname(excusa))
        seleccion_mes = request.POST.get('mes_seleccionado')
        if seleccion_mes != None and seleccion_mes != "":
            request.session['mes_seleccionado'] = seleccion_mes
        editar = request.POST.get('Editar')
        if editar != None and editar != "":
            aprendiz = json.loads(Usuario.objects.get(N_Documento=editar).toJSON())
            aprendiz['id'] = json.loads(Aprendiz.objects.get(N_Documento_A_id=editar).toJSON()).get('id')
            request.session['aprendiz'] =  aprendiz
            return redirect('/edit_assis/')
    if 'mes_seleccionado' not in request.session:
        cxt['mes_seleccionado'] = obtener_fecha_actual().get('numero')[5:7]
    else:
        cxt['mes_seleccionado'] = request.session['mes_seleccionado']
    return authenticate_instru(request, "Instructor/Registro_de_Asistencias.html", cxt)

def Editar_Asistencia(request):
    aprendiz = request.session['aprendiz']
    especialidad = request.session['especialidad']
    asistencias = list(Asistencia.objects.filter(Aprendiz_id=aprendiz['id'], Especialidad_id=especialidad))
    estados = list(Estado_Asistencia.objects.all())
    estados_t = {}
    asistencias_t = {}
    conteo = {'si':0, 'no':0}
    id = 1
    for est in estados:
        estados_t['est_' + str(id)] = json.loads(Estado_Asistencia.objects.get(id=est.id).toJSON())
        id = id+1
    id = 1
    for asis in asistencias:
        asistencia = json.loads(Asistencia.objects.get(id=asis.id).toJSON())
        dia = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[8:]
        mes = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[5:7]
        año = json.loads(Asistencia.objects.get(id=asis.id).toJSON()).get('Date_Asistencia')[:4]
        asistencia['fecha'] = {'dia':dia, 'mes':mes, 'año':año}
        if Excusa.objects.filter(Asistencia_id=asistencia['id']).exists():
            asistencia['excusa'] = json.loads(Excusa.objects.get(Asistencia_id=asistencia['id']).toJSON()).get('Soporte_Excusa')
        else:
            asistencia['excusa'] = ""
        asistencias_t['asis_' + str(id)] = asistencia
        if asistencias_t['asis_' + str(id)].get('Estado_Asistencia_id') == 1:
            conteo['si'] = conteo['si']+1
        else:
            conteo['no'] = conteo['no']+1
        id = id+1
    aprendiz['conteo'] = conteo
    aprendiz['estados_t'] = estados_t
    aprendiz['asistencias_t'] = asistencias_t
    aprendiz['especialidad'] = especialidad
    aprendiz['ficha'] = request.session['ficha']
    if request.method == 'POST':
        ficha = request.POST.get('ficha')
        especialidad = request.POST.get('especialidad')
        if ficha != None and ficha != "":
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=ficha).toJSON())
            request.session['especialidad'] = especialidad
            return redirect('/register_assis/')
        asistencia = request.POST.get('asis')
        estado = request.POST.get('estado')
        notes = request.POST.get('Notes')
        if request.POST.get('Cambio_asis') == "100":
            print("si")
            print(estado)
            Asistencia.objects.filter(id=asistencia).update(Estado_Asistencia_id=estado, Notes=notes)
            return redirect('/edit_assis/')
    return authenticate_instru(request, "Instructor/Editar_Asistencia.html", aprendiz)

# MODULO ADMIN

def Registrar_Apre(request):
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt = {}
    cxt['documentos_t'] = documentos_t
    cxt['ficha'] = request.session['ficha']
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        F_last_name = request.POST.get('F_last_name')
        S_last_name = request.POST.get('S_last_name')
        Phone_number = request.POST.get('Phone_number')
        N_Documento = request.POST.get('N_Documento')
        Inst_mail = request.POST.get('Inst_mail')
        Person_mail = request.POST.get('Person_mail')
        T_Documento = request.POST.get('Documento')
        Date = request.POST.get('Date')
        if first_name != "" and first_name != None and F_last_name != None and F_last_name != "" and Phone_number != "" and Phone_number != None and N_Documento != None and N_Documento != "" and Inst_mail != "" and Inst_mail != None and T_Documento != None and T_Documento != "0":
            if not(Usuario.objects.filter(N_Documento=N_Documento).exists()):
                newUser = Usuario(first_name=first_name, second_name=second_name, F_last_name=F_last_name, S_last_name=S_last_name,
                                  Phone_number=Phone_number, Person_mail=Person_mail, Inst_mail=Inst_mail, Date=Date,
                                  Documento=Documento.objects.get(id=T_Documento), N_Documento=N_Documento, Rol=Rol.objects.get(id='1'))
                newUser.save()
                newApre = Aprendiz(N_Documento_A=Usuario.objects.get(
                    N_Documento=N_Documento), Ficha=Ficha.objects.get(number_F=request.session['ficha'].get('number_F')))
                newApre.save()
                breakpoint()
            else:
                messages.error(request, '¡ERROR! El Aprendiz con el numero de documento: ' + N_Documento + ' ya existe', {
                })
        else:
            messages.error(request, '¡ERROR! Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Registrar_Aprendiz.html", cxt)


def Listado_Apre(request):
    aprendices = filtrar_listado(request)
    aprendiz = {}
    tabla = {}
    id = 1
    for dato in aprendices:
        aprendiz = json.loads(Usuario.objects.get(N_Documento=dato.N_Documento_A_id).toJSON())
        aprendiz['num'] = id
        tabla['appr_' + str(id)] = aprendiz
        id = id+1
    cxt = {'tabla': tabla}
    ficha = request.session['ficha']
    ficha['programa'] = json.loads(Programa.objects.get(id=ficha['Programa_id']).toJSON()).get('name_P')
    cxt['ficha'] = ficha
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Usuario.objects.filter(N_Documento=delete).delete()
            return redirect('/list_stu/')
        if editar != "" and editar != None:
            request.session['appr'] = Usuario.objects.get(
                N_Documento=editar).toJSON()
            return redirect('/edit_appr/')
    return authenticate_admin(request, "Administrador/Listado_de_Aprendices.html", cxt)


def Editar_Apre(request):
    appr = json.loads(request.session['appr'])
    appr['aviso'] = '¡ERROR'
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    appr['documentos_t'] = documentos_t
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        F_last_name = request.POST.get('F_last_name')
        S_last_name = request.POST.get('S_last_name')
        Phone_number = request.POST.get('Phone_number')
        N_Documento = request.POST.get('N_Documento')
        Inst_mail = request.POST.get('Inst_mail')
        Person_mail = request.POST.get('Person_mail')
        T_Documento = request.POST.get('Documento')
        Date = request.POST.get('Date')
        if first_name != "" and first_name != None and F_last_name != None and F_last_name != "" and Phone_number != "" and Phone_number != None and N_Documento != None and N_Documento != "" and Inst_mail != "" and Inst_mail != None and T_Documento != None and T_Documento != "0":
            if not(Usuario.objects.filter(N_Documento=N_Documento).exists()) or N_Documento == json.loads(request.session['appr']).get('N_Documento'):
                Usuario.objects.filter(N_Documento=json.loads(request.session['appr']).get('N_Documento')).update(first_name=first_name, second_name=second_name, F_last_name=F_last_name, S_last_name=S_last_name,
                                                                                                                  Phone_number=Phone_number, Person_mail=Person_mail, Inst_mail=Inst_mail, Date=Date,
                                                                                                                  Documento=Documento.objects.get(id=T_Documento), N_Documento=N_Documento, Rol=Rol.objects.get(id='1'))
                return redirect('/list_stu/')
            else:
                messages.error(request, 'El Aprendiz con el numero de documento: ' + N_Documento + ' ya existe', {
                })
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Aprendiz.html", appr)

def Registro_Documento(request):
    documentos = list(Documento.objects.all())
    documento = {}
    tabla = {}
    id = 1
    for dato in documentos:
        documento = json.loads(Documento.objects.get(name_T_Document=dato.name_T_Document).toJSON())
        documento['num'] = id
        tabla['doc_' + str(id)] = documento
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Documento.objects.filter(name_T_Document=delete).delete()
            return redirect('/register_document/')
        if add != "" and add != None:
            name = request.POST.get('name')
            sigla = request.POST.get('sigla')
            if name != "" and sigla != "":
                newDocument = Documento(name_T_Document=name, acronym_D=sigla)
                newDocument.save()
            return redirect('/register_document/')
        if editar != "" and editar != None:
            request.session['documento'] = Documento.objects.get(name_T_Document=editar).toJSON()
            return redirect('/edit_doc/')
    return authenticate_admin(request, "Administrador/Registro_de_Documentos.html", cxt)


def Editar_Documento(request):
    documento = json.loads(request.session['documento'])
    documento['aviso'] = '¡ERROR!'
    if request.method == 'POST':
        name = request.POST.get('name_T_Document')
        siglas = request.POST.get('acronym_D')
        if name != None and name != "" and siglas != "" and siglas != None:
            Documento.objects.filter(name_T_Document=json.loads(request.session['documento']).get('name_T_Document')).update(name_T_Document=name, acronym_D=siglas)
            return redirect('/register_document/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Documento.html", documento)


def Especialidades(request):
    especialidades = list(Especialidad.objects.all().filter(N_Ficha_id=request.session['ficha'].get('id')))
    instructores = list(Instructor.objects.all())
    fichas = list(Ficha.objects.all())
    trimestres = list(Trimestre.objects.all().order_by('name_Tri'))
    especialidad = {}
    fichas_t = {}
    especialidades_t = {}
    instructores_t = {}
    trimestres_t = {}
    cxt = {}
    id = 1
    for dato in especialidades:
        especialidad = json.loads(Especialidad.objects.get(id=dato.id).toJSON())
        especialidad['num'] = id
        especialidades_t['pro_' + str(id)] = especialidad
        id = id+1
    id = 1
    for dato in instructores:
        instructor = json.loads(Usuario.objects.get(N_Documento=dato.N_Documento_I_id).toJSON())
        instructor['id'] = dato.id
        instructores_t['ins_' + str(id)] = instructor
        id = id+1
    id = 1
    for dato in fichas:
        fichas_t['fic_' + str(id)] = json.loads(Ficha.objects.get(number_F=dato.number_F).toJSON())
        id = id+1
    id = 1
    for dato in trimestres:
        trimestres_t['tri_' + str(id)] = json.loads(Trimestre.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt['especialidades_t'] = especialidades_t
    cxt['instructores_t'] = instructores_t
    cxt['fichas_t'] = fichas_t
    cxt['trimestres_t'] = trimestres_t
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Especialidad.objects.filter(id=delete).delete()
            return redirect('/specialties/')
        if add != "" and add != None:
            name_E = request.POST.get('name_E')
            Days_E = request.POST.get('Days_E')
            Time_Begining = request.POST.get('Time_Begining')
            Time_Ending = request.POST.get('Time_Ending')
            Time_Begining = Time_Begining + ":00"
            Time_Ending = Time_Ending + ":00"
            Instructor_id = request.POST.get('Instructor_id')
            Trimestre_id = request.POST.get('Trimestre_id')
            ficha = request.session['ficha']
            if name_E != "" and Days_E != "" and Time_Begining != "" and Time_Ending != "" and Instructor_id != "" and Trimestre_id != "":
                newEspecialidad = Especialidad(name_E=name_E,Days_E=Days_E, Time_Begining=Time_Begining, Time_Ending=Time_Ending, Instructor_id=Instructor_id, N_Ficha_id=ficha['id'], Trimestre_id=Trimestre_id)
                newEspecialidad.save()
            return redirect('/specialties/')
        if editar != "" and editar != None:
            request.session['especialidad'] = Especialidad.objects.get(id=editar).toJSON()
            return redirect('/edit_especialidad/')
    return authenticate_admin(request, "Administrador/Especialidades_Asociadas.html", cxt)

def Editar_Especialidad(request):
    cxt = json.loads(request.session['especialidad'])
    instructores = list(Instructor.objects.all())
    trimestres = list(Trimestre.objects.all().order_by('name_Tri'))
    instructores_t = {}
    trimestres_t = {}
    id = 1
    for dato in instructores:
        instructor = json.loads(Usuario.objects.get(N_Documento=dato.N_Documento_I_id).toJSON())
        instructor['id'] = dato.id
        instructores_t['ins_' + str(id)] = instructor
        id = id+1
    id = 1
    for dato in trimestres:
        trimestres_t['tri_' + str(id)] = json.loads(Trimestre.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt['instructores_t'] = instructores_t
    cxt['trimestres_t'] = trimestres_t
    cxt['aviso'] = '¡ERROR'
    if request.method == 'POST':
        name = request.POST.get('name_E')
        Days_E = request.POST.get('Days_E')
        Time_Begining = request.POST.get('Time_Begining')
        Time_Ending = request.POST.get('Time_Ending')
        Instructor_id = request.POST.get('Instructor_id')
        Trimestre_id = request.POST.get('Trimestre_id')
        if name != None and name != "" and Days_E != "" and Days_E != None and Time_Begining != None and Time_Begining != "" and Time_Ending != None and Time_Ending != "":
            Especialidad.objects.filter(id=json.loads(request.session['especialidad']).get('id')).update(
                name_E=name, Days_E=Days_E, Time_Begining=Time_Begining, Time_Ending=Time_Ending, Instructor_id=Instructor.objects.get(id=Instructor_id), Trimestre_id=Trimestre.objects.get(id=Trimestre_id))
            return redirect('/specialties/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Especialidad.html", cxt)
    

def Registro_Estado(request):
    estados = list(Estado_Asistencia.objects.all())
    estado = {}
    tabla = {}
    id = 1
    for dato in estados:
        estado = json.loads(Estado_Asistencia.objects.get(name_E_Asis=dato.name_E_Asis).toJSON())
        estado['num'] = id
        tabla['est_' + str(id)] = estado
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Estado_Asistencia.objects.filter(name_E_Asis=delete).delete()
            return redirect('/register_status/')
        if add != "" and add != None:
            name = request.POST.get('name_E_Asist')
            if name != "" and name != None:
                newEstado = Estado_Asistencia(name_E_Asis=name)
                newEstado.save()
            return redirect('/register_status/')
        if editar != "" and editar != None:
            request.session['estado'] = Estado_Asistencia.objects.get(name_E_Asis=editar).toJSON()
            return redirect('/edit_est/')
    return authenticate_admin(request, "Administrador/Registro_de_Estado.html", cxt)

def Editar_Estado_de_Asistencia(request):
    estado = json.loads(request.session['estado'])
    estado['aviso'] = '¡ERROR!'
    if request.method == 'POST':
        name = request.POST.get('name_E_Asis')
        if name != None:
            Estado_Asistencia.objects.filter(name_E_Asis=json.loads(request.session['estado']).get('name_E_Asis')).update(name_E_Asis=name)
            return redirect('/register_status/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Estado_de_Asistencia.html", estado)

def Registro_Ficha(request):
    fichas = list(Ficha.objects.all().order_by('number_F'))
    programas = list(Programa.objects.all())
    jornadas = list(Jornada.objects.all())
    sedes = list(Sede.objects.all())
    ficha = {}
    fichas_t = {}
    programas_t = {}
    jornadas_t = {}
    sedes_t = {}
    cxt = {}
    id = 1
    for dato in fichas:
        ficha = json.loads(Ficha.objects.get(number_F=dato.number_F).toJSON())
        ficha['num'] = id
        fichas_t['fic_' + str(id)] = ficha
        id = id+1
    id = 1
    for dato in programas:
        programas_t['pro_' + str(id)] = json.loads(Programa.objects.get(id=dato.id).toJSON())
        id = id+1
    id = 1
    for dato in jornadas:
        jornadas_t['jor_' + str(id)] = json.loads(Jornada.objects.get(id=dato.id).toJSON())
        id = id+1
    id = 1
    for dato in sedes:
        sedes_t['sed_' + str(id)] = json.loads(Sede.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt['fichas_t'] = fichas_t
    cxt['programas_t'] = programas_t
    cxt['jornadas_t'] = jornadas_t
    cxt['sedes_t'] = sedes_t
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        ficha = request.POST.get('Ficha')
        if delete != "" and delete != None:
            Ficha.objects.filter(number_F=delete).delete()
            return redirect('/register_file/')
        if add != "" and add != None:
            number_f = request.POST.get('number_F')
            Jornada_id = request.POST.get('Jornada_id')
            Sede_id = request.POST.get('Sede_id')
            Programa_id = request.POST.get('Programa_id')
            if number_f != "" and number_f != None and Jornada_id != "" and Jornada_id != None and Sede_id != None and Sede_id != "" and Programa_id != "" and Programa_id != None:
                newFicha = Ficha(number_F=number_f,Jornada_id=Jornada_id, Sede_id=Sede_id, Programa_id=Programa_id )
                newFicha.save()
            else:
                messages.error(request, '¡ERROR! Debes completar todos los campos')
            return redirect('/register_file/')
        if editar != "" and editar != None:
            request.session['ficha'] = Ficha.objects.get(number_F=editar).toJSON()
            return redirect('/edit_ficha/')
        if ficha != "" and ficha != None:
            request.session['ficha'] = json.loads(Ficha.objects.get(number_F=ficha).toJSON())
            return redirect('/list_stu/')
    return authenticate_admin(request, "Administrador/Registro_de_Fichas.html", cxt)


def Editar_Ficha(request):
    programas = list(Programa.objects.all())
    jornadas = list(Jornada.objects.all())
    sedes = list(Sede.objects.all())
    programas_t = {}
    jornadas_t = {}
    sedes_t = {}
    cxt ={}
    id = 1
    for dato in programas:
        programas_t['pro_' + str(id)] = json.loads(Programa.objects.get(id=dato.id).toJSON())
        id = id+1
    id = 1
    for dato in jornadas:
        jornadas_t['jor_' + str(id)] = json.loads(Jornada.objects.get(id=dato.id).toJSON())
        id = id+1
    id = 1
    for dato in sedes:
        sedes_t['sed_' + str(id)] = json.loads(Sede.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt['programas_t'] = programas_t
    cxt['jornadas_t'] = jornadas_t
    cxt['sedes_t'] = sedes_t
    cxt['ficha'] = json.loads(request.session['ficha'])
    cxt['aviso'] = '¡ERROR'
    if request.method == 'POST':
        Jornadas = request.POST.get('Jornada')
        Sedes = request.POST.get('Sede')
        Programas = request.POST.get('Programa')
        if Jornada != None and Jornada != "" and Sede != "" and Sede != None and Programa != None and Programa != "":
            Ficha.objects.filter(number_F=json.loads(request.session['ficha']).get('number_F')).update(Jornada_id=Jornada.objects.get(id=Jornadas), Sede_id=Sede.objects.get(id=Sedes), Programa_id=Programa.objects.get(id=Programas))
            return redirect('/register_file/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Ficha.html", cxt)

def Registro_Grupo(request):
    grupos = list(Grupo.objects.all())
    grupo = {}
    tabla = {}
    id = 1
    for dato in grupos:
        grupo = json.loads(Grupo.objects.get(Name_Group=dato.Name_Group).toJSON())
        grupo['num'] = id
        tabla['doc_' + str(id)] = grupo
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Grupo.objects.filter(Name_Group=delete).delete()
            return redirect('/register_group/')
        if add != "" and add != None:
            Name_Group = request.POST.get('Name_Group')
            if Name_Group != "":
                newGrupo = Grupo(Name_Group=Name_Group)
                newGrupo.save()
            return redirect('/register_group/')
        if editar != "" and editar != None:
            request.session['grupo'] = Grupo.objects.get(Name_Group=editar).toJSON()
            return redirect('/edit_group/')
    return authenticate_admin(request, "Administrador/Registro_de_Grupo.html", cxt)

def Editar_Grupo(request):
    grupo = json.loads(request.session['grupo'])
    grupo['aviso'] = '¡ERROR!'
    if request.method == 'POST':
        name = request.POST.get('Name_Group')
        if name != None:
            Grupo.objects.filter(Name_Group=json.loads(request.session['grupo']).get('Name_Group')).update(Name_Group=name)
            return redirect('/register_group/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Grupo.html", grupo)

def Registrar_Ins(request):
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    cxt = {}
    cxt['documentos_t'] = documentos_t
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        F_last_name = request.POST.get('F_last_name')
        S_last_name = request.POST.get('S_last_name')
        Phone_number = request.POST.get('Phone_number')
        N_Documento = request.POST.get('N_Documento')
        Inst_mail = request.POST.get('Inst_mail')
        Person_mail = request.POST.get('Person_mail')
        T_Documento = request.POST.get('Documento')
        Date = request.POST.get('Date')
        if first_name != "" and first_name != None and F_last_name != None and F_last_name != "" and Phone_number != "" and Phone_number != None and N_Documento != None and N_Documento != "" and Inst_mail != "" and Inst_mail != None and T_Documento != None and T_Documento != "0":
            if not(Usuario.objects.filter(N_Documento=N_Documento).exists()):
                newUser = Usuario(first_name=first_name, second_name=second_name, F_last_name=F_last_name, S_last_name=S_last_name,
                                  Phone_number=Phone_number, Person_mail=Person_mail, Inst_mail=Inst_mail, Date=Date,
                                  Documento=Documento.objects.get(id=T_Documento), N_Documento=N_Documento, Rol=Rol.objects.get(id=2))
                newUser.save()
                newIns = Instructor(N_Documento_I=Usuario.objects.get(
                    N_Documento=N_Documento), Password="")
                newIns.save()
                breakpoint()
            else:
                messages.error(request, '¡ERROR! El Instructor con el numero de documento: ' + N_Documento + ' ya existe', {
                })
        else:
            messages.error(request, '¡ERROR! Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Registrar_Instructor.html", cxt)

def Registro_Instructor(request):
    instructores = list(Usuario.objects.all().filter(Rol=Rol.objects.get(id=2)))
    instructor = {}
    tabla = {}
    id = 1
    for dato in instructores:
        instructor = json.loads(Usuario.objects.get(N_Documento=dato.N_Documento).toJSON())
        instructor['num'] = id
        tabla['ins_' + str(id)] = instructor
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Usuario.objects.filter(N_Documento=delete).delete()
            return redirect('/register_ins/')
        if editar != "" and editar != None:
            request.session['ins'] = Usuario.objects.get(N_Documento=editar).toJSON()
            return redirect('/edit_ins/')
    return authenticate_admin(request, "Administrador/Registro_de_Instructores.html", cxt)

def Editar_Ins(request):
    ins = json.loads(request.session['ins'])
    ins['aviso'] = '¡ERROR'
    documentos = list(Documento.objects.all())
    documentos_t = {}
    id = 1
    for dato in documentos:
        documentos_t['doc_' + str(id)] = json.loads(Documento.objects.get(id=dato.id).toJSON())
        id = id+1
    ins['documentos_t'] = documentos_t
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        F_last_name = request.POST.get('F_last_name')
        S_last_name = request.POST.get('S_last_name')
        Phone_number = request.POST.get('Phone_number')
        N_Documento = request.POST.get('N_Documento')
        Inst_mail = request.POST.get('Inst_mail')
        Person_mail = request.POST.get('Person_mail')
        T_Documento = request.POST.get('Documento')
        Date = request.POST.get('Date')
        if first_name != "" and first_name != None and F_last_name != None and F_last_name != "" and Phone_number != "" and Phone_number != None and N_Documento != None and N_Documento != "" and Inst_mail != "" and Inst_mail != None and T_Documento != None and T_Documento != "0":
            if not(Usuario.objects.filter(N_Documento=N_Documento).exists()) or N_Documento == json.loads(request.session['ins']).get('N_Documento'):
                Usuario.objects.filter(N_Documento=json.loads(request.session['ins']).get('N_Documento')).update(first_name=first_name, second_name=second_name, F_last_name=F_last_name, S_last_name=S_last_name,
                                                                                                                  Phone_number=Phone_number, Person_mail=Person_mail, Inst_mail=Inst_mail, Date=Date,
                                                                                                                  Documento=Documento.objects.get(id=T_Documento), N_Documento=N_Documento)
                return redirect('/register_ins/')
            else:
                messages.error(request, 'El Aprendiz con el numero de documento: ' + N_Documento + ' ya existe', {
                })
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Instructor.html", ins)

def Registro_Jornada(request):
    jornadas = list(Jornada.objects.all())
    jornada = {}
    tabla = {}
    id = 1
    for dato in jornadas:
        jornada = json.loads(Jornada.objects.get(name_J=dato.name_J).toJSON())
        jornada['num'] = id
        tabla['doc_' + str(id)] = jornada
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Jornada.objects.filter(name_J=delete).delete()
            return redirect('/register_jornada/')
        if add != "" and add != None:
            name = request.POST.get('name_J')
            sigla = request.POST.get('acronym_J')
            if name != "" and sigla != "":
                newJornada = Jornada(name_J=name,acronym_J=sigla)
                newJornada.save()
            return redirect('/register_jornada/')
        if editar != "" and editar != None:
            request.session['jornada'] = Jornada.objects.get(name_J=editar).toJSON()
            return redirect('/edit_jorn/')
    return authenticate_admin(request, "Administrador/Registro_de_Jornadas.html", cxt)

def Editar_Jornada(request):
    jornada = json.loads(request.session['jornada'])
    jornada['aviso'] = '¡ERROR!'
    if request.method == 'POST':
        name = request.POST.get('name_J')
        siglas = request.POST.get('acronym_J')
        if name != None:
            Jornada.objects.filter(name_J=json.loads(request.session['jornada']).get('name_J')).update(name_J=name, acronym_J=siglas)
            return redirect('/register_jornada/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Jornada.html", jornada)

    
def Registro_Programa(request):
    programas = list(Programa.objects.all())
    programa = {}
    tabla = {}
    id = 1
    for dato in programas:
        programa = json.loads(Programa.objects.get(name_P=dato.name_P).toJSON())
        programa['num'] = id
        tabla['doc_' + str(id)] = programa
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Programa.objects.filter(name_P=delete).delete()
            return redirect('/register_program/')
        if add != "" and add != None:
            name_P = request.POST.get('name_P')
            sigla = request.POST.get('acronym_P') 
            if name_P != "" and sigla != "":
                newPrograma = Programa(name_P=name_P, acronym_P=sigla)
                newPrograma.save()
            return redirect('/register_program/') 
        if editar != "" and editar != None:
            request.session['programa'] = Programa.objects.get(name_P=editar).toJSON()
            return redirect('/edit_program/')
    return authenticate_admin(request, "Administrador/Registro_de_Programas.html", cxt) 
    
def Editar_Programa(request):
    programa = json.loads(request.session['programa'])
    programa['aviso'] = '¡ERROR!'
    if request.method == 'POST':
        name = request.POST.get('name_P')
        sigla = request.POST.get('acronym_P')
        print(name)
        if name != None and  name != "":
            Programa.objects.filter(name_P=json.loads(request.session['programa']).get('name_P')).update(name_P=name,acronym_P=sigla)
            return redirect('/register_program/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Programa.html", programa)

def Registro_Sede(request): 
    sedes = list(Sede.objects.all())
    sede = {}
    tabla = {} 
    id = 1
    for dato in sedes:          
        sede = json.loads(Sede.objects.get(name_S=dato.name_S).toJSON())
        sede['num'] = id
        tabla['doc_' + str(id)] = sede
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Sede.objects.filter(name_S=delete).delete()
            return redirect('/register_campus/')
        if add != "" and add != None:
            name = request.POST.get('name_S')
            Direccion = request.POST.get('address_S')
            Ciudad = request.POST.get('city_S')
            if name != "" and Direccion != "" and Ciudad != "":
                newSede = Sede(name_S=name, address_S=Direccion, city_S=Ciudad)
                newSede.save()
            return redirect('/register_campus/')
        if editar != "" and editar != None:
            request.session['sede'] = Sede.objects.get(name_S=editar).toJSON()
            return redirect('/edit_sed/')
    return authenticate_admin(request, "Administrador/Registro_de_Sedes.html", cxt)

def Editar_Sede(request):
    sede = json.loads(request.session['sede'])
    sede['aviso'] = '¡ERROR!'
    if request.method == 'POST':
        name = request.POST.get('name_S')
        print(name)
        sigla = request.POST.get('address_S')
        ciudad = request.POST.get('city_S')
        if name != None and  name != "" and ciudad != None and ciudad != "":
            Sede.objects.filter(name_S=json.loads(request.session['sede']).get('name_S')).update(name_S=name,address_S=sigla,city_S=ciudad)
            return redirect('/register_campus/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Sede.html", sede)

def Registro_Trimestre(request):
    trimestres = list(Trimestre.objects.all().order_by('name_Tri'))
    trimestre = {}
    tabla = {}
    id = 1
    for dato in trimestres:
        trimestre = json.loads(Trimestre.objects.get(name_Tri=dato.name_Tri).toJSON())
        trimestre['num'] = id
        tabla['Tri_' + str(id)] = trimestre
        id = id+1
    cxt = {'tabla': tabla}
    if request.method == 'POST':
        delete = request.POST.get('Eliminar')
        add = request.POST.get('Añadir')
        editar = request.POST.get('Editar')
        if delete != "" and delete != None:
            Trimestre.objects.filter(name_Tri=delete).delete()
            return redirect('/register_trimester/')
        if add != "" and add != None:
            name = request.POST.get('name_Tri')
            if name != "":
                newDocument = Trimestre(name_Tri=name)
                newDocument.save()
            return redirect('/register_trimester/')
        if editar != "" and editar != None:
            request.session['trimestre'] = Trimestre.objects.get(name_Tri=editar).toJSON()
            return redirect('/edit_trimester/')
    return authenticate_admin(request, "Administrador/Registro_de_Trimestres.html",cxt)

def Editar_Trimestre(request):
    trimestre = json.loads(request.session['trimestre'])
    trimestre['aviso'] = '¡ERROR!'
    if request.method == 'POST':
        name = request.POST.get('name_Tri')
        print(name)
        if name != None and  name != "":
            Trimestre.objects.filter(name_Tri=json.loads(request.session['trimestre']).get('name_Tri')).update(name_Tri=name)
            return redirect('/register_trimester/')
        else:
            messages.error(request, 'Debes llenar todos los campos obligatorios', {
            })
    return authenticate_admin(request, "Administrador/Editar/Editar_Trimestre.html", trimestre)
