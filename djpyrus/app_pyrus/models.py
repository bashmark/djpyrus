import re
from django.db import models

class RevisionModel(models.Model):
    revision = models.PositiveIntegerField(verbose_name='revision')


class ChainModel(models.Model):
    name = models.CharField(max_length=300, verbose_name='chain name', blank=True, null=True)
    address = models.CharField(max_length=500, verbose_name='chain address')
    login = models.CharField(max_length=300, verbose_name='login')
    password = models.CharField(max_length=300, verbose_name='password')
    port = models.CharField(max_length=10, verbose_name="port")
    scheme = models.CharField(max_length=5, verbose_name="scheme")
    version = models.CharField(max_length=10, verbose_name="version", blank=True, null=True)

    def save(self, *args, **kwargs):
        RevisionModel.objects.filter(id=1).update(revision=RevisionModel.objects.get(id=1).revision + 1)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        RevisionModel.objects.filter(id=1).update(revision=RevisionModel.objects.get(id=1).revision + 1)
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.address)


class RmsModel(models.Model):
    name = models.CharField(max_length=300, verbose_name='rms name')
    address = models.CharField(max_length=500, verbose_name='rms address')
    login = models.CharField(max_length=300, verbose_name='login')
    password = models.CharField(max_length=300, verbose_name='password', blank=True, null=True)
    port = models.CharField(max_length=10, verbose_name="port")
    scheme = models.CharField(max_length=5, verbose_name="scheme")
    version = models.CharField(max_length=10, verbose_name="version", blank=True, null=True)
    chain = models.ForeignKey(ChainModel, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        RevisionModel.objects.filter(id=1).update(revision=RevisionModel.objects.get(id=1).revision + 1)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        RevisionModel.objects.filter(id=1).update(revision=RevisionModel.objects.get(id=1).revision + 1)
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.address)


class RemotesModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='remote_name', blank=True, null=True)
    remote = models.CharField(max_length=200, verbose_name='remote', blank=True, null=True)
    password = models.CharField(max_length=200, verbose_name='password', blank=True, null=True)
    rms = models.ForeignKey(RmsModel, on_delete=models.CASCADE, related_name='remote', blank=True, null=True)
    chain = models.ForeignKey(ChainModel, on_delete=models.CASCADE, related_name='remote', blank=True, null=True)

    def __str__(self):
        return str([re.sub(r' ', '', str(self.remote)), self.name, self.password])

    # class Meta:
    #     unique_together = [['rms', 'remote'], ['chain', 'remote']]


class AccessToken(models.Model):
    access_token = models.CharField(max_length=1000, verbose_name='access token')

    def __str__(self):
        return str(self.access_token)
