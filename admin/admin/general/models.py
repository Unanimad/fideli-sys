from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=50)
    playStore = models.URLField()
    appStore = models.URLField()
    status = models.BooleanField(default=1)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=16)
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Cliente'

    def __str__(self):
        return self.name


class CardConfiguration(models.Model):
    expire = models.IntegerField()
    limit = models.IntegerField()
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Configuração do cartão'
        verbose_name_plural = 'Configurações dos cartões'

    def __str__(self):
        return 'Expira: ' + self.expire + ' / Limite:' + self.limit


class Service(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'


class Card(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company)
    client = models.ForeignKey(Client)
    service = models.ForeignKey(Service)
    configuration = models.ForeignKey(CardConfiguration)

    class Meta:
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'

    def __str__(self):
        return str(self.int)
