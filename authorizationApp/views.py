from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from ShopApp.views import index

from django.core.mail import send_mail
from django.http import HttpResponse

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, "account/login.html")
def register(request):
    if request.method == "POST":
        password =request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            print("пароли не совпадают")
            return redirect(request, 'account/login.html')

        username = request.POST.get("username")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким логином уже существует")
            render(request, "account/login.html")
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            send_mail(
                'Подтверждение электронной почты',
                'Если регистрацию проводили не вы, то проигнорируйте это письмо.',
                'gameshopgames12@gmail.com',
                [email],
                fail_silently=False,  # Если ошибка, показать ее
            )
            user.save()
            login(request, user)
            return redirect(index)
        except Exception as e:
            messages.error(request, "Ошибка при регистрации")
            return render(request, 'account/login.html')
