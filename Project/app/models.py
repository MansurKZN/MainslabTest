from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)

class Organization(models.Model):
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)

    class Meta:
        unique_together = ['client_name', 'name']

class Bill(models.Model):
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    number = models.IntegerField()
    sum = models.FloatField()
    date = models.DateField()
    service = models.CharField(max_length=500)
    fraud_score = models.FloatField()
    service_class = models.IntegerField()
    service_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['client_org', 'number']