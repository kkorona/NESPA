from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def submission(request):
    return render(request, 'submission.html')