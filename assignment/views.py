from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def submission(request):
    if request.method == "GET":
        return render(request, 'submission.html')
        
    if request.method == "POST":
        prob_ID = request.POST.get('',None)
        