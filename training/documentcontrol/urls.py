from django.urls import path
from . import views

app_name = "documentcontrol"

urlpatterns = [
    path("upload", views.upload_document, name="upload"),
    path("all_documents", views.all_documents, name="all_documents"),
    path("<doc_id>", views.display_document, name="display_document"),
]