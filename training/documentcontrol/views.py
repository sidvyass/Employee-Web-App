from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import DocumentForm
import os
from .models import Documents

def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        saving_directory = r"C:\pythonprojects\training_app\training\media\documentcontrol\documents"

        if form.is_valid():
            all_files = [filename for filename in os.listdir(saving_directory)]
            if request.FILES['file'].name.replace(" ", "_") not in all_files:
                form.save()
            return HttpResponseRedirect(reverse("documentcontrol:all_documents"))

    else:
        form = DocumentForm()
    return render(request, "documentcontrol/upload.html", {'form':form})

def display_document(request, doc_id):
    # doc = Documents.objects.get(pk=doc_id)
    return HttpResponse("no")

def all_documents(request):
    return render(request, "documentcontrol/document_list.html", {"documents":Documents.objects.all()})