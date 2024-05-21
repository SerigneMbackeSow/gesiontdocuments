from django.urls import path

from .views import login_page, logout_page, signup_page, seconnecter, deconnecter

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('signup/', signup_page, name='signup'),
    path('seconnecter/', seconnecter, name='signupc'),
    path('deconnecter/<int:id>', deconnecter, name='signupc'),
]
