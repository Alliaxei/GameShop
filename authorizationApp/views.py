from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, user_logged_out
from django.contrib import messages
from ShopApp.views import index

from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR password is incorrect')
    return render(request, "account/login.html")
def register(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            print("пароли не совпадают")
            return redirect(request, 'account/login.html')

        username = request.POST.get("username")
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            print("Такйо email занят")
            messages.error(request, "Пользователь с таким email уже существует")
            return redirect('login')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким логином уже существует")
            return render(request, "account/login.html")
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            try:
                confirm_url = request.build_absolute_uri(reverse('verify_email', args=[uid, token]))
            except Exception as e:
                print(e)
                confirm_url = None

            send_mail(
                'Подтверждение электронной почты',
                f'Для подтверждения вашего email , перейдите по следующей ссылке: {confirm_url}',
                'gameshopgames12@gmail.com',
                [email],
                fail_silently=False,  # Если ошибка, показать ее
            )
            user.save()


            return JsonResponse({'status': 'success'})
        except Exception as e:
            messages.error(request, "Ошибка при регистрации" + str(e))
            return render(request, 'account/login.html')
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, user)
            return render(request, 'account/email.html')
        else:
            return HttpResponse("Некорректная ссылка для подтверждения email.")
    except Exception as e:
        return HttpResponse(f"Произошла ошибка: {str(e)}")
@login_required
def profile_view(request):
    return render(request, 'account/profile/profile.html')

@login_required
def edit_profile(request):
    return render(request, 'account/profile/edit_profile.html')

@login_required
def delete_account(request):
    return render(request, 'account/profile/delete_account.html')

@login_required
def payment_view(request):
    return render(request, 'account/profile/payments.html')