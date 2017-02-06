from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nome')
    playStore = models.URLField(blank=True, null=True)
    appStore = models.URLField(blank=True, null=True)
    status = models.BooleanField(default=1)
    image = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nome')
    phone = models.CharField(max_length=14, verbose_name='Telefone')
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Cliente'

    def __str__(self):
        return self.name


class CardConfiguration(models.Model):
    expire = models.IntegerField(verbose_name='Válidade do cartão em dias')
    limit = models.IntegerField(verbose_name='Limite de pontos para troca')
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Configuração do cartão'
        verbose_name_plural = 'Configurações dos cartões'

    def __str__(self):
        return 'Expira: ' + str(self.expire) + ' dias / Limite: ' + str(self.limit) + ' pontos.'


class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nome')
    reward = models.CharField(max_length=200, verbose_name='Recompensa')
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.name


class Card(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    converted = models.BooleanField(default=0, verbose_name='Convertido?')
    company = models.ForeignKey(Company)
    client = models.ForeignKey(Client)
    service = models.ForeignKey(Service, verbose_name='Serviço')
    configuration = models.ForeignKey(CardConfiguration, verbose_name='Configuração')

    class Meta:
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'

    def __str__(self):
        return '# ' + str(self.int)
