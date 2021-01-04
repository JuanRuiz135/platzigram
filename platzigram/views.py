""" Main views """

# Django
from django.http import HttpResponse

def hi(request):
    # Returns a hi msg

    return HttpResponse(str('Hi'))