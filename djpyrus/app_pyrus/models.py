from django.db import models


class ChainModel(models.Model):
    name = models.CharField(max_length=300, verbose_name='chain name')
    address = models.CharField(max_length=500, verbose_name='chain address')
    port = models.CharField(max_length=10, verbose_name="port")
    scheme = models.CharField(max_length=5, verbose_name="scheme")
    version = models.CharField(max_length=10, verbose_name="version")

    def __str__(self):
        return str(self.name)


class RmsModel(models.Model):
    name = models.CharField(max_length=300, verbose_name='rms name')
    address = models.CharField(max_length=500, verbose_name='rms address')
    port = models.CharField(max_length=10, verbose_name="port")
    scheme = models.CharField(max_length=5, verbose_name="scheme")
    version = models.CharField(max_length=10, verbose_name="version")
    chain = models.ForeignKey(ChainModel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.name)
