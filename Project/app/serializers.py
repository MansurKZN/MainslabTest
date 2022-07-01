from django.db.models import Count, Sum
from rest_framework import serializers

from app.models import Client, Bill


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class ClientSerializer(serializers.ModelSerializer):
    organizations_count = serializers.SerializerMethodField('org_count')
    all_organizatons_sum = serializers.SerializerMethodField('org_sum')

    def org_count(self, obj):
        return Bill.objects.filter(client_name=obj.id).aggregate(Count('number')).get('number__count')

    def org_sum(self, obj):
        return Bill.objects.filter(client_name=obj.id).aggregate(Sum('sum')).get('sum__sum')

    class Meta:
        model = Client
        fields = ['name', 'organizations_count', 'all_organizatons_sum']

class BillSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client_name.name')
    client_org = serializers.CharField(source='client_org.name')

    class Meta:
        model = Bill
        fields = ['client_name', 'client_org', 'number', 'sum', 'date', 'service', 'fraud_score', 'service_class', 'service_name']

class BillFilterSerializer(serializers.Serializer):
    organization = serializers.CharField(required=False)
    client = serializers.CharField(required=False)