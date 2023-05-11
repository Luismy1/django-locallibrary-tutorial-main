from django.shortcuts import render

# Create your views here.

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .models import MyUser

def add_user(request):
    if request.method == 'POST':
        user_type = request.POST['user_type']
        credits = request.POST['credits']
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if request.user.user_type == MyUser.ADMIN:
            if user_type != MyUser.DISTRIBUTOR:
                messages.error(request, 'Solo puedes agregar distribuidores')
                return redirect('add_user')

        if request.user.user_type == MyUser.DISTRIBUTOR:
            if user_type != MyUser.CLIENT:
                messages.error(request, 'Solo puedes agregar clientes')
                return redirect('add_user')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e)
            return redirect('add_user')

        try:
            MyUser.objects.create_user(
                user_type=user_type,
                credits=credits,
                name=name,
                email=email,
                username=username,
                password=password,
            )
            messages.success(request, 'Usuario agregado exitosamente')
            return redirect('add_user')
        except:
            messages.error(request, 'Ocurrió un error al agregar el usuario')
            return redirect('add_user')

    return render(request, 'add_user.html')


