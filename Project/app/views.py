import openpyxl
from rest_framework.response import Response
from rest_framework.views import APIView

from app.helpers import fraudDetector, serviceClassifier
from app.models import Client, Organization, Bill
from app.serializers import FileUploadSerializer, ClientSerializer, BillSerializer, BillFilterSerializer


class ClientOrgUpload(APIView):
    serializer_class = FileUploadSerializer

    def post(self, request):
        review = FileUploadSerializer(data=request.data)
        if not review.is_valid():
            return Response({"error": "file upload error"}, status=400)
        try:
            excel_file = openpyxl.load_workbook(request.FILES['file'])
            client_sheet = excel_file['client']
            org_sheet = excel_file['organization']
            for row in client_sheet.rows:
                if row[0].row == 1 or row[0].value == None:
                    continue
                for elem in row:
                    Client.objects.get_or_create(name=elem.value)

            for row in org_sheet.rows:
                if row[0].row == 1 or row[0].value == None:
                    continue
                client = Client.objects.get(name=row[0].value)
                Organization.objects.get_or_create(client_name=client, name=row[1].value, address=row[2].value)
        except:
            return Response({"error": "file parse error"}, status=400)
        return Response({"message": "successfully"}, status=200)

class BillsUpload(APIView):
    serializer_class = FileUploadSerializer

    def post(self, request):
        review = FileUploadSerializer(data=request.data)
        if not review.is_valid():
            return Response({"error": "file upload error"}, status=400)
        try:
            excel_file = openpyxl.load_workbook(request.FILES['file'])
            file = excel_file.active
            for row in file.rows:
                if row[0].row == 1 or row[0].value == None:
                    continue
                client = Client.objects.get(name=row[0].value)
                org = Organization.objects.get(name=row[1].value)
                fs = fraudDetector(row[5].value)
                classifier = serviceClassifier(row[5].value)
                try:
                    Bill.objects.get_or_create(client_name=client, client_org=org, number=row[2].value, sum=row[3].value,
                                               date=row[4].value, service=row[5].value, fraud_score=fs, service_class=list(classifier.keys())[0], service_name=classifier.get(list(classifier.keys())[0]))
                except:
                    pass
        except:
            return Response({"error": "file parse error"}, status=400)
        return Response({"message": "successfully"}, status=200)


class ClientsList(APIView):

    def get(self, request):
        serialize = Client.objects.all()
        result = ClientSerializer(serialize, many=True).data
        return Response(result)


class BillsList(APIView):
    serializer_class = BillFilterSerializer

    def get(self, request):
        serialize = Bill.objects.all()
        result = BillSerializer(serialize, many=True).data
        return Response(result)

    def post(self, request):
        review = BillFilterSerializer(data=request.data)
        if not review.is_valid():
            return Response({"error": "error"}, status=400)
        if review.data.get('organization') and review.data.get('client'):
            serialize = Bill.objects.filter(client_org__name=review.data.get('organization'), client_name__name=review.data.get('client'))
        elif review.data.get('client'):
            serialize = Bill.objects.filter(client_name__name=review.data.get('client'))
        elif review.data.get('organization'):
            serialize = Bill.objects.filter(client_org__name=review.data.get('organization'))
        else:
            serialize = Bill.objects.all()
        result = BillSerializer(serialize, many=True).data
        return Response(result)
