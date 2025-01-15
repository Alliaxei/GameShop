from django.contrib import admin
from django.urls import path, include
from ShopApp.views import *
from authorizationApp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_window, name='index'),
    path('main/', main_window, name='main'),
    # path('main/extended_info<int:game_id>/', extended_view, name='extended_info'),
    path('catalog/extended_info<int:game_id>/', extended_view, name='extended_info'),
    path('cart/', cart_view, name='cart'),
    path('contacts/', contacts, name='contacts'),
    path('about/', about, name='about'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/ajax/search/', ajax_search_games, name='ajax_search_games'),
    path('accounts/login', login_view, name='login'),
    path('accounts/', include('allauth.urls')),
    path("register/", register, name="register"),
    path("profile/", edit_profile, name='profile'),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/delete/", delete_account, name="delete_account"),
    path("profile/payments/", payment_view, name='payments'),
    path('remove/',remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('add_to_cart_form/', add_to_cart_form, name='add_to_cart_form'),
    path('verify_email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('apply_filters/', apply_filters, name='apply_filters'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
