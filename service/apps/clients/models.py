from django.db import models


class Client(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.PROTECT)
    company_name = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)

    def __str__(self):
        return f'id: {self.id}, company name: {self.company_name}'