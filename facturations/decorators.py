# decorators.py
from django.views.decorators.csrf import csrf_exempt

def csrf_exempt_all(view_func):
    return csrf_exempt(view_func)
