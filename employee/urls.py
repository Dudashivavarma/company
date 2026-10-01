from django.urls import include, path
from . import views
urlpatterns = [
    path('',views.entry_page),
    path('home/',views.home),
    path('dark/',views.dark_theme),
    path('delete/',views.delete),
    path('register/',views.register),
    path('login/',views.login_in),
    path('update/',views.update),
    path('display/',views.disaply),
    path('send/',views.sending_mail),
    path('store/',views.store),
    path('middle/',views.middleware)
]
