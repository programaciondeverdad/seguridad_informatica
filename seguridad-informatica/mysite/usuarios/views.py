from django.http import HttpResponse

from django.shortcuts import render, redirect
#Importamos el logout
from django.contrib.auth import logout as do_logout
from django.template import loader

# Importamos librerías de AuthenticationForm para que haga el login solo. Nosotros solamente validaremos
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login

# Formulario de registro
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .forms import ValidacionCodigoForm
from .models import ValidacionCodigo

import datetime

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "usuarios/welcome.html")
    # En otro caso redireccionamos al login
    return redirect('login_path')

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('login_path')


"""
Las passwords de los usuarios por default ya se envian y se guardan encriptadas a la base de datos
Trabajan con el ALGORITMO PBKDF2 con el hash SHA256.
Esta combinación ya de por si es MUY SEGURA.
"""
def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()

    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Crear el registro en la tabla
                codigo_seguro = '12345678'
                validacion_pendiente = ValidacionCodigo.objects.create(codigo=codigo_seguro, 
                                                                       usuario = user, 
                                                                       date_init = datetime.date.today())
                validacion_pendiente.save()
                validacion_codigo = ValidacionCodigo.objects.filter(
                                                                    codigo=codigo_seguro
                                                            ).filter(
                                                                    usuario = user, 
                                                            ).filter(
                                                                    date_init=datetime.date.today()
                                                            )
                # TODO: Enviar e-mail de validacion

                # Formulario de validacion de codigo
                formCheck = ValidacionCodigoForm(instance=validacion_codigo[0])

                # enviar a la pagina de validacion de codigo
                return render(request, "usuarios/check_login.html", {'form': formCheck})

    # Si llegamos al final renderizamos el formulario 
    return checkValidacionLogin(request)



def checkValidacionLogin(request):
    # Formulario de validacion de codigo
    formCheck = ValidacionCodigoForm()


    if request.method == "POST":

        User = get_user_model()
        usuario = User.objects.get(pk=request.POST.get('usuario'))

        validacion_codigo = ValidacionCodigo.objects.filter(
                                                            codigo=request.POST.get('codigo_ingresado')
                                                    ).filter(
                                                            usuario = usuario)


        # Si la validacion_codigo no la encuentra, el usuario no ingreso el codigo correcto
        if not list(validacion_codigo):
            form = AuthenticationForm()
            return render(request, "usuarios/login.html", {'form': form})
        else:
        # Si la validacion_codigo la encontró entonces loguear al usuario
            # return HttpResponse(formCheck.errors)

            if usuario is not None:
                do_login(request,usuario)

                return redirect('dashboard')

    form = AuthenticationForm()
    return render(request, "usuarios/login.html", {'form': form})

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si queremos borramos los campos de ayuda
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    # Si llegamos al final renderizamos el formulario
    return render(request, "usuarios/register.html", {'form': form})


def dashboard(request):
    return render(request, "usuarios/dashboard.html")
