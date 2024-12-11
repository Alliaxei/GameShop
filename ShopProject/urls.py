from django.contrib import admin
from django.urls import path, include
from ShopApp.views import *
from authorizationApp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('main/', main_window, name='main'),
    path('cart/', cart_view, name='cart'),
    path('contacts/', contacts, name='contacts'),
    path('about/', about, name='about'),
    path('catalog/', catalog, name='catalog'),
    path('accounts/login', login_view, name='login'),
    path('accounts/', include('allauth.urls')),
    path("register/", register, name="register"),
    path('remove/',remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
