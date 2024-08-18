from django.urls import path

from .views import login_page, logout_page, signup_page, seconnecter, deconnecter, acceulli_page, redirige_app

urlpatterns = [
    #path('login/', login_page, name='login'),
    path('login/', acceulli_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('signup/', signup_page, name='signup'),
    path('seconnecter/', seconnecter, name='signupc'),
    path('deconnecter/<int:id>', deconnecter, name='signupc'),
path('acceulli_pagen/', acceulli_page, name='login'),
path('redirige_app/<str:app>', redirige_app, name='redirige_app'),
]
