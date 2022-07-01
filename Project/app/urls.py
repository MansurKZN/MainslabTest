from django.urls import path

from app.views import ClientOrgUpload, BillsUpload, ClientsList, BillsList

urlpatterns = [
    path('upload/client_org/', ClientOrgUpload.as_view()),
    path('upload/bills/', BillsUpload.as_view()),
    path('clients/', ClientsList.as_view()),
    path('bills/', BillsList.as_view()),
]