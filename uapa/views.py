from django.http import HttpResponse
from django.shortcuts import render


def Test(request):
    value = "http://" + request.META['HTTP_HOST']
    return HttpResponse('Result: ' + value)